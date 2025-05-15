# class_b.py
from sqlalchemy import Column, Integer, String,ForeignKey
from app.database import Base


class ClassB(Base):
    __tablename__ = 'class_b'
    id = Column(Integer, primary_key=True)
    description = Column(String)

    # Define the reverse relationship (backref)
    class_a_id = Column(Integer, ForeignKey('class_a.id'))