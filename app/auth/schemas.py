from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):

    username: str

    email: EmailStr

    password: str

    role: str = "Analyst"


class LoginRequest(BaseModel):

    username: str

    password: str