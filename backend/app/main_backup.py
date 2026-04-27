from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.applied_job import AppliedJob
from app.core.database import Base, engine
from app.api.v1 import match, resume, recommend
from app.models.profile import Profile
from app.api.v1 import apply
from app.api.v1 import actions
from app.api.v1.auth import router as auth_router  # ← ADD THIS

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])  # ← ADD THIS
app.include_router(match.router)
app.include_router(resume.router)
app.include_router(recommend.router)
app.include_router(apply.router)
app.include_router(actions.router)

@app.get("/")
def home():
    return {"message": "Backend Running"}
