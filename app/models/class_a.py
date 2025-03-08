# class_a.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

class ClassA(Base):
    __tablename__ = 'class_a'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define a relationship with ClassB
    model_details = relationship('ClassB', backref='class_a', lazy='dynamic')