from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    skills = Column(Text)
    raw_text = Column(Text)
