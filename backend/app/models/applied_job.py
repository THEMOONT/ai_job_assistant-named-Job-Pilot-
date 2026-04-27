from sqlalchemy import Column, Integer, String
from app.core.database import Base


class AppliedJob(Base):
    __tablename__ = "applied_jobs"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer)
    title = Column(String)
    company = Column(String)
    source = Column(String)
    apply_link = Column(String)
    status = Column(String, default="Applied")
