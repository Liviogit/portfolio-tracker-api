from sqlalchemy.orm import Session
from models.user_model import User

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, first_name: str, last_name: str, username: str, hashed_password: str) -> User:
    # Vérifie si l'utilisateur existe déjà
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return None

    db_user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session,user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

