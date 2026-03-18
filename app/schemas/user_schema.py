from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)
    role: str = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True