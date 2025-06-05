from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import or_

Base = declarative_base()

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50))  # 'youtube' ou 'site web'
    titre = Column(String(200))
    url = Column(String(300))
    tags = Column(String(200))  # ex: 'Deep Learning,PySpark,,Machine Learning,Reseaux de neurones



    @staticmethod
    def extract_tags_from_question(question: str):
        question = question.lower()
        tags = []
        if "deep learning" in question:
            tags.append("Deep Learning")
        if "pyspark" in question:
            tags.append("PySpark")
        if "ml" in question:
            tags.append("Machine Learning")
        # Ajoute d'autres règles selon tes besoins
        return tags
    

    @staticmethod
    def get_additional_resources(db: Session, context_tags: list):
        if not context_tags:
            return []
        filters = [Resource.tags.ilike(f"%{tag}%") for tag in context_tags]
        return db.query(Resource).filter(or_(*filters)).all()