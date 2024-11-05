# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return crud.create_user(db=db, user=user)

@router.put("/profile/{user_id}", response_model=schemas.User)
def update_profile(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return crud.update_user_profile(db=db, user_id=user_id, username=user.username, email=user.email)
