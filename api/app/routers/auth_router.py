from fastapi import APIRouter, Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from services.security import create_access_token, hash_password
from services.auth_service import authenticate_user, get_current_user
from services.user_service import create_user
from database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class UserOut(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    username: str

@auth_router.post("/register", response_model=UserOut)
def register(user: UserRegister, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = create_user(db, user.first_name, user.last_name, user.username, hashed_password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    return db_user

@auth_router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    return get_current_user(token, db)
