from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

SAVED_JOBS = []
APPLIED_JOBS = []

class JobPayload(BaseModel):
    profile_id: int
    jobs: list

class SavePayload(BaseModel):
    profile_id: int
    job: dict


@router.post("/save-job")
def save_job(data: SavePayload):

    SAVED_JOBS.append(data.job)

    return {"message": "saved"}


@router.get("/saved-jobs/{profile_id}")
def saved_jobs(profile_id: int):
    return SAVED_JOBS


@router.post("/bulk-apply")
def bulk_apply(data: JobPayload):

    for job in data.jobs:

        APPLIED_JOBS.append({
            "title": job.get("title"),
            "company": job.get("company"),
            "status": "Applied",
            "source": job.get("source"),
            "apply_link": job.get("apply_link")
        })

    return {
        "message": "applications submitted",
        "count": len(data.jobs)
    }


@router.get("/applied-jobs/{profile_id}")
def applied_jobs(profile_id: int):
    return APPLIED_JOBS


@router.get("/dashboard-stats/{profile_id}")
def dashboard_stats(profile_id: int):

    return {
        "saved_jobs": len(SAVED_JOBS),
        "applied_jobs": len(APPLIED_JOBS),
        "match_score": 91,
        "jobs_found": 18
    }
