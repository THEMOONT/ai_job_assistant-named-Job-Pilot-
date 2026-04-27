from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api.v1 import auth
from app.api.v1 import actions
from app.api.v1 import recommend
from app.api.v1 import resume

# Import DB + Models
from app.core.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JobPilot API",
    version="1.0.0"
)

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route
@app.get("/")
def home():
    return {
        "message": "🚀 JobPilot Backend Running"
    }

# Register APIs
app.include_router(auth.router)
app.include_router(actions.router)
app.include_router(recommend.router)
app.include_router(resume.router)
