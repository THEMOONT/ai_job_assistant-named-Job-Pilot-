from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.models.applied_job import AppliedJob
from app.models.saved_job import SavedJob
from app.core.database import Base, engine
from app.api.v1 import match, resume, recommend
from app.models.profile import Profile
from app.api.v1 import apply
from app.api.v1 import actions
from app.api.v1.auth import router as auth_router
from app.core.logger import api_logger, error_logger
import time

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        duration = round((time.time() - start) * 1000)
        api_logger.info(
            f"{request.method} {request.url.path} "
            f"status={response.status_code} "
            f"duration={duration}ms "
            f"ip={request.client.host}"
        )
        return response
    except Exception as e:
        error_logger.error(f"Request failed: {request.method} {request.url.path} - {str(e)}")
        raise


app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(match.router)
app.include_router(resume.router)
app.include_router(recommend.router)
app.include_router(apply.router)
app.include_router(actions.router)


@app.get("/")
def home():
    api_logger.info("Home endpoint hit")
    return {"message": "Backend Running"}
