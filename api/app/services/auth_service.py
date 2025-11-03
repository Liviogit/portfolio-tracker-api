from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime
from services.security import SECRET_KEY, ALGORITHM, verify_password
from services.user_service import get_user_by_username
from models.user_model import User


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Vérifie si l'utilisateur existe et si le mot de passe est correct.
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        return None
    return user


def get_current_user(token: str, db: Session) -> User:
    """
    Récupère l'utilisateur courant à partir du token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
