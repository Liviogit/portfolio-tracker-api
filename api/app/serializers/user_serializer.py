from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
class UserCreate(UserBase):
    pass