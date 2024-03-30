from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///teachers.db')
Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    feedback = relationship("Feedback", back_populates="teacher")

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    text = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    
    teacher = relationship("Teacher", back_populates="feedback")


Base.metadata.create_all(engine)
