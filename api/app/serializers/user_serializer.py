from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    user_id: int

    class Config:
        orm_mode = True  # ✅ permet de convertir directement depuis un objet SQLAlchemy
