from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.models.applied_job import AppliedJob
from app.core.logger import apply_logger, error_logger

router = APIRouter()


class JobItem(BaseModel):
    title: str
    company: str
    source: str
    apply_link: str
    match_score: int = 0
    location: str = ""


class BulkApplyPayload(BaseModel):
    profile_id: int
    jobs: list[JobItem]


@router.post("/bulk-apply")
def bulk_apply(data: BulkApplyPayload):
    apply_logger.info(f"Bulk apply request - profile_id: {data.profile_id}, jobs: {len(data.jobs)}")

    if not data.jobs:
        apply_logger.warning(f"Bulk apply failed - no jobs provided for profile_id: {data.profile_id}")
        raise HTTPException(status_code=400, detail="No jobs provided")

    db = SessionLocal()
    try:
        for job in data.jobs:
            row = AppliedJob(
                profile_id=data.profile_id,
                title=job.title,
                company=job.company,
                source=job.source,
                apply_link=job.apply_link,
                status="Applied"
            )
            db.add(row)
            apply_logger.info(f"Applied to: {job.title} at {job.company} for profile_id: {data.profile_id}")

        db.commit()
        apply_logger.info(f"Bulk apply complete - profile_id: {data.profile_id}, total: {len(data.jobs)}")
        return {"message": "Jobs applied successfully", "count": len(data.jobs)}

    except Exception as e:
        db.rollback()
        error_logger.error(f"Bulk apply failed - profile_id: {data.profile_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to apply to jobs")
    finally:
        db.close()
