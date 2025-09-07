from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


