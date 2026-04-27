from fastapi import APIRouter
from app.services.match_engine import calculate_match_score

router = APIRouter()

@router.get("/match")
def match():
    score = calculate_match_score(
        semantic=0.9,
        keyword=0.8,
        experience=1
    )

    return {"match_score": score}
