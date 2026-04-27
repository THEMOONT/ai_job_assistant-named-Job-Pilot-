from fastapi import APIRouter, UploadFile, File
from app.services.resume_parser import parse_resume
from app.services.ai_resume_parser import parse_resume_with_ai
from app.services.skill_extractor import extract_skills
from app.models.profile import Profile
from app.core.database import SessionLocal

router = APIRouter()


@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    content = await file.read()

    text = parse_resume(content, file.content_type)

    # Local free skill extraction
    local_skills = extract_skills(text)

    try:
        profile = parse_resume_with_ai(text[:10000])

        ai_skills = profile.get("skills", [])

        merged_skills = sorted(
            list(set(ai_skills + local_skills))
        )

        profile["skills"] = merged_skills

    except Exception:
        profile = {
            "name": "Unknown",
            "skills": local_skills,
            "experience_years": 0,
            "domain": "Unknown",
            "note": "AI quota not available, using local parser"
        }

    # Save profile in PostgreSQL
    db = SessionLocal()

    new_profile = Profile(
        filename=file.filename,
        skills=",".join(profile["skills"]),
        raw_text=text[:5000]
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    profile_id = new_profile.id

    db.close()

    return {
        "profile_id": profile_id,
        "filename": file.filename,
        "profile": profile,
        "text_preview": text[:1000]
    }


@router.get("/profile/{profile_id}")
def get_profile(profile_id: int):

    db = SessionLocal()

    profile = db.query(Profile).filter(
        Profile.id == profile_id
    ).first()

    db.close()

    if not profile:
        return {"error": "Profile not found"}

    return {
        "id": profile.id,
        "filename": profile.filename,
        "skills": profile.skills.split(","),
        "raw_text_preview": profile.raw_text[:500]
    }
