from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    raw_text = Column(Text)
    skills = Column(Text)
    domain = Column(String(100))
