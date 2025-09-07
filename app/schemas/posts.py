from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostCreateModel(BaseModel):
    title: str
    content: str
    published : Optional[bool] = False

class PostUpdateModel(PostCreateModel):
    pass

class PostOutModel(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner_id: int
    created_at: datetime
    class Config: from_attributes = True




