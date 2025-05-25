from pydantic import BaseModel, EmailStr, Field

class UserCreateDTO(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)
    user_type: str
    is_enabled: bool = True

class UserUpdateDTO(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    user_type: str
    is_enabled: bool

class UserResponseDTO(BaseModel):
    id: str
    name: str
    email: str
    user_type: str
    is_enabled: bool
    created_at: str
    updated_at: str 