from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from app.schemas.users import UserOutModel, UserCreateModel
from app.models.users import User
from app.db.database import get_db
from app.schemas.token import Token
from app.core.security import verify_password, create_access_token, get_current_user, hash_password

router = APIRouter()

@router.get("/", response_model=List[UserOutModel])
async def get_all_users(db : Session = Depends(get_db), user = Depends(get_current_user)):
    users = db.query(User).all()
    return users

@router.get("/{id}", response_model=UserOutModel)
async def get_user(id: int, db : Session = Depends(get_db), user = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/", response_model=UserOutModel, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    hashed_password = hash_password(user.password)
    new_user = User(**user.model_dump(exclude={"password"}), password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Incorrect credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



