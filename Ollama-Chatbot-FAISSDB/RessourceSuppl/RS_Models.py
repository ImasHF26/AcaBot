from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

DATABASE_URL = "sqlite:///./bdd/chatbot_metadata.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50))
    titre = Column(String(200))
    url = Column(String(300))
    tags = Column(String(200))

    @staticmethod
    def extract_tags_from_question(question: str):
        question = question.lower()
        tags = []
        if "deep learning" in question:
            tags.append("Deep Learning")
        if "pyspark" in question:
            tags.append("PySpark")
        if "ml" in question or "machine learning" in question:
            tags.append("Machine Learning")
        return tags

    @staticmethod
    def get_additional_resources(db: Session, context_tags: list):
        if not context_tags:
            return []
        filters = [Resource.tags.ilike(f"%{tag}%") for tag in context_tags]
        return db.query(Resource).filter(or_(*filters)).all()

class ResourceCreate(BaseModel):
    type: str
    titre: str
    url: str
    tags: Optional[str] = ""

class ResourceOut(BaseModel):
    id: int
    type: str
    titre: str
    url: str
    tags: Optional[str] = ""

    class Config:
        from_attributes = True