from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.posts import PostOutModel, PostUpdateModel, PostCreateModel
from app.db.database import get_db
from app.models.posts import Post
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PostOutModel])
async def get_all_posts(db: Session = Depends(get_db), user = Depends(get_current_user), skip: int = 0, limit: int = 10, search: Optional[str] = ""):
    posts = db.query(Post).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model=PostOutModel)
async def get_post(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.post("/", response_model=PostOutModel, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreateModel, db: Session = Depends(get_db), user = Depends(get_current_user)):
    new_post = Post(**post.model_dump(), owner_id = user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}", response_model=PostOutModel)
async def update_post(id: int, post: PostUpdateModel, db: Session = Depends(get_db), user = Depends(get_current_user)):
    db_post = db.query(Post).filter(Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if db_post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this post")
    update_data = post.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




