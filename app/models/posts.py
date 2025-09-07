from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean,func, ForeignKey
from app.db.database import Base

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String)
    content = Column(Text)
    published = Column(Boolean)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

