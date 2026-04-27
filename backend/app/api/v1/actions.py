from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.models.saved_job import SavedJob
from app.models.applied_job import AppliedJob
from app.core.logger import actions_logger, error_logger

router = APIRouter()


class SavePayload(BaseModel):
    profile_id: int
    job: dict


@router.post("/save-job")
def save_job(data: SavePayload):
    actions_logger.info(f"Save job request - profile_id: {data.profile_id}, job: {data.job.get('title')}")
    db = SessionLocal()
    try:
        job = data.job
        row = SavedJob(
            profile_id=data.profile_id,
            title=job.get("title", ""),
            company=job.get("company", ""),
            location=job.get("location", ""),
            source=job.get("source", ""),
            apply_link=job.get("apply_link", ""),
            match_score=job.get("match_score", 0)
        )
        db.add(row)
        db.commit()
        actions_logger.info(f"Job saved successfully - profile_id: {data.profile_id}, title: {job.get('title')}")
        return {"message": "Job saved"}
    except Exception as e:
        db.rollback()
        error_logger.error(f"Save job failed - profile_id: {data.profile_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save job")
    finally:
        db.close()


@router.get("/saved-jobs/{profile_id}")
def saved_jobs(profile_id: int):
    actions_logger.info(f"Fetch saved jobs - profile_id: {profile_id}")
    db = SessionLocal()
    try:
        rows = db.query(SavedJob).filter(SavedJob.profile_id == profile_id).all()
        actions_logger.info(f"Returned {len(rows)} saved jobs for profile_id: {profile_id}")
        return [
            {
                "id": r.id,
                "title": r.title,
                "company": r.company,
                "location": r.location,
                "source": r.source,
                "apply_link": r.apply_link,
                "match_score": r.match_score
            }
            for r in rows
        ]
    except Exception as e:
        error_logger.error(f"Fetch saved jobs failed - profile_id: {profile_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch saved jobs")
    finally:
        db.close()


@router.get("/applied-jobs/{profile_id}")
def applied_jobs(profile_id: int):
    actions_logger.info(f"Fetch applied jobs - profile_id: {profile_id}")
    db = SessionLocal()
    try:
        rows = db.query(AppliedJob).filter(AppliedJob.profile_id == profile_id).all()
        actions_logger.info(f"Returned {len(rows)} applied jobs for profile_id: {profile_id}")
        return [
            {
                "id": r.id,
                "title": r.title,
                "company": r.company,
                "source": r.source,
                "status": r.status,
                "apply_link": r.apply_link
            }
            for r in rows
        ]
    except Exception as e:
        error_logger.error(f"Fetch applied jobs failed - profile_id: {profile_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch applied jobs")
    finally:
        db.close()


@router.get("/dashboard-stats/{profile_id}")
def dashboard_stats(profile_id: int):
    actions_logger.info(f"Fetch dashboard stats - profile_id: {profile_id}")
    db = SessionLocal()
    try:
        saved_count = db.query(SavedJob).filter(SavedJob.profile_id == profile_id).count()
        applied_count = db.query(AppliedJob).filter(AppliedJob.profile_id == profile_id).count()
        return {
            "saved_jobs": saved_count,
            "applied_jobs": applied_count,
            "match_score": 91,
            "jobs_found": 18
        }
    except Exception as e:
        error_logger.error(f"Dashboard stats failed - profile_id: {profile_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch stats")
    finally:
        db.close()
