from fastapi import APIRouter, HTTPException, Query
from app.models.profile import Profile
from app.core.database import SessionLocal
import os
import time
import asyncio
import logging
import httpx
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

router = APIRouter()

RAPID_KEY = os.getenv("RAPIDAPI_KEY")
ADZUNA_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_KEY = os.getenv("ADZUNA_APP_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("recommend")

CACHE = {}
CACHE_SECONDS = 600


# ---------------------------------------------------
# CACHE CLEAN
# ---------------------------------------------------
def cleanup_cache():

    now = time.time()

    expired = []

    for key, value in CACHE.items():
        if now - value["time"] > CACHE_SECONDS:
            expired.append(key)

    for key in expired:
        del CACHE[key]


# ---------------------------------------------------
# COUNTRY MAP
# ---------------------------------------------------
COUNTRY_MAP = {
    "india": "in",
    "in": "in",
    "us": "us",
    "usa": "us",
    "uk": "gb",
    "canada": "ca",
    "australia": "au",
    "any": "in"
}


# ---------------------------------------------------
# ROLE DETECTION
# ---------------------------------------------------
def build_search_keyword(user_skills):

    text = " ".join(user_skills).lower()

    if "production support" in text:
        return "Production Support Engineer"

    if "application support" in text:
        return "Application Support Engineer"

    if "technical support" in text:
        return "Technical Support Engineer"

    if "oracle" in text or "pl/sql" in text:
        return "Oracle DBA"

    if "linux" in text:
        return "Linux Engineer"

    if "aws" in text:
        return "Cloud Support Engineer"

    if "python" in text:
        return "Python Developer"

    return "Software Engineer"


# ---------------------------------------------------
# BAD TITLES FILTER
# ---------------------------------------------------
BAD_WORDS = [
    "director",
    "sales",
    "artist",
    "creative",
    "marketing",
    "designer",
    "finance",
    "account executive",
    "vp",
    "manager retail"
]


GOOD_WORDS = [
    "support",
    "linux",
    "sql",
    "oracle",
    "cloud",
    "engineer",
    "production",
    "application",
    "technical",
    "operations",
    "incident",
    "devops",
    "database"
]


def is_relevant_job(title):

    t = str(title).lower()

    for bad in BAD_WORDS:
        if bad in t:
            return False

    for good in GOOD_WORDS:
        if good in t:
            return True

    return False


# ---------------------------------------------------
# SCORING
# ---------------------------------------------------
def calculate_score(user_skills, job, role):

    score = 0

    title = str(job.get("title", "")).lower()
    desc = str(job.get("description", "")).lower()

    if role.lower() in title:
        score += 40

    for skill in user_skills:

        s = skill.lower()

        if s in title:
            score += 20

        elif s in desc:
            score += 10

    # role boosts
    boosts = [
        "support",
        "linux",
        "oracle",
        "sql",
        "production",
        "cloud"
    ]

    for word in boosts:
        if word in title:
            score += 8

    return min(score, 100)


# ---------------------------------------------------
# JSEARCH
# ---------------------------------------------------
async def fetch_jsearch(client, keyword):

    try:

        r = await client.get(
            "https://jsearch.p.rapidapi.com/search",
            headers={
                "X-RapidAPI-Key": RAPID_KEY,
                "X-RapidAPI-Host":
                "jsearch.p.rapidapi.com"
            },
            params={
                "query": keyword,
                "page": "1",
                "num_pages": "1"
            }
        )

        if r.status_code == 200:

            data = r.json().get("data", [])

            jobs = []

            for x in data:

                jobs.append({
                    "source": "JSearch",
                    "title": x.get("job_title"),
                    "company": x.get("employer_name"),
                    "location": x.get("job_city"),
                    "country": x.get("job_country"),
                    "description":
                        x.get("job_description"),
                    "apply_link":
                        x.get("job_apply_link")
                })

            return jobs

    except Exception as e:
        logger.error(e)

    return []


# ---------------------------------------------------
# REMOTEOK
# ---------------------------------------------------
async def fetch_remoteok(client):

    try:

        r = await client.get(
            "https://remoteok.com/api",
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if r.status_code == 200:

            data = r.json()[1:10]

            jobs = []

            for x in data:

                jobs.append({
                    "source": "RemoteOK",
                    "title": x.get("position"),
                    "company": x.get("company"),
                    "location": "Remote",
                    "country": "Global",
                    "description":
                        x.get("description"),
                    "apply_link":
                        x.get("url")
                })

            return jobs

    except Exception as e:
        logger.error(e)

    return []


# ---------------------------------------------------
# MAIN API
# ---------------------------------------------------
@router.get("/recommended-jobs/{profile_id}")
async def recommended_jobs(
    profile_id: int,
    country: str = Query("India"),
    city: str = Query(None)
):

    cleanup_cache()

    db = SessionLocal()

    try:

        profile = db.query(Profile).filter(
            Profile.id == profile_id
        ).first()

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )

        user_skills = [
            x.strip()
            for x in profile.skills.split(",")
            if x.strip()
        ]

        role = build_search_keyword(user_skills)

        keyword = role

        if city:
            keyword += " " + city
        else:
            keyword += " " + country

        cache_key = str(profile_id) + keyword

        if cache_key in CACHE:

            item = CACHE[cache_key]

            if time.time() - item["time"] < CACHE_SECONDS:
                return item["data"]

        async with httpx.AsyncClient(
            timeout=8
        ) as client:

            res = await asyncio.gather(
                fetch_jsearch(client, keyword),
                fetch_remoteok(client)
            )

        jobs = []
        jobs.extend(res[0])
        jobs.extend(res[1])

        results = []

        for job in jobs:

            title = job["title"]

            if not is_relevant_job(title):
                continue

            score = calculate_score(
                user_skills,
                job,
                role
            )

            if score < 40:
                continue

            results.append({
                "source": job["source"],
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "country": job["country"],
                "apply_link":
                    job["apply_link"],
                "match_score": score
            })

        # Naukri
        slug = keyword.lower().replace(" ", "-")

        results.append({
            "source": "Naukri",
            "title": role,
            "company": "Search Jobs",
            "location": city or country,
            "country": country,
            "apply_link":
                "https://www.naukri.com/"
                + slug + "-jobs",
            "match_score": 85
        })

        # LinkedIn
        results.append({
            "source": "LinkedIn",
            "title": role,
            "company": "Search Jobs",
            "location": city or country,
            "country": country,
            "apply_link":
                "https://www.linkedin.com/jobs/search/?keywords="
                + quote_plus(keyword),
            "match_score": 80
        })

        results.sort(
            key=lambda x: x["match_score"],
            reverse=True
        )

        response = {
            "profile_id": profile.id,
            "filename": profile.filename,
            "search_keyword": keyword,
            "skills": user_skills,
            "total_jobs_found": len(results),
            "jobs": results[:20]
        }

        CACHE[cache_key] = {
            "time": time.time(),
            "data": response
        }

        return response

    finally:
        db.close()
