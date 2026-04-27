from fastapi import APIRouter
from app.core.database import SessionLocal
from app.models.applied_job import AppliedJob

router = APIRouter()


@router.post("/bulk-apply")
def bulk_apply(data: dict):

    db = SessionLocal()

    jobs = data["jobs"]
    profile_id = data["profile_id"]

    for job in jobs:

        row = AppliedJob(
            profile_id=profile_id,
            title=job["title"],
            company=job["company"],
            source=job["source"],
            apply_link=job["apply_link"],
            status="Applied"
        )

        db.add(row)

    db.commit()
    db.close()

    return {
        "message": "Jobs Applied Successfully",
        "count": len(jobs)
    }


@router.get("/applied-jobs/{profile_id}")
def applied_jobs(profile_id: int):

    db = SessionLocal()

    rows = db.query(AppliedJob).filter(
        AppliedJob.profile_id == profile_id
    ).all()

    db.close()

    result = []

    for x in rows:
        result.append({
            "id": x.id,
            "title": x.title,
            "company": x.company,
            "source": x.source,
            "status": x.status,
            "apply_link": x.apply_link
        })

    return result
