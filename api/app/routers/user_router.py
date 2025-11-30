from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.user_model import User
from services.auth_service import get_current_user
from database import get_db
from services.user_service import create_user, get_user
from serializers.user_serializer import UserCreate, UserBase

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", response_model=UserBase)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@user_router.get("/", response_model=UserBase)
def read_user(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = get_user(db,current_user.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
