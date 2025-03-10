from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True)
    sender = Column(String)
    subject = Column(String)
    content = Column(String)
    category = Column(String)
    confidence = Column(Float)
    processed_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    response = relationship("Response", back_populates="email")

class Response(Base):
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, ForeignKey('emails.id'))
    content = Column(String)
    generated_at = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String)
    
    email = relationship("Email", back_populates="response") 