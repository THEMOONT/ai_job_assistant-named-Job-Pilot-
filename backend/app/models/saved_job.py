from sqlalchemy import Column, Integer, String
from app.core.database import Base


class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String, default="")
    source = Column(String)
    apply_link = Column(String)
    match_score = Column(Integer, default=0)
