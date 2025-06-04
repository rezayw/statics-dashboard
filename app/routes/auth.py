from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.crud.user import get_user_by_email, create_user, verify_password
from app.auth.jwt_handler import create_access_token

router = APIRouter()


# ====[ Schema ]====
class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ====[ Register Endpoint ]====
@router.post("/register")
def register(payload: RegisterRequest):
    if get_user_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    create_user(
        email=payload.email,
        full_name=payload.full_name,
        password=payload.password
    )

    return {"msg": "User created successfully"}


# ====[ Login Endpoint ]====
@router.post("/login")
def login(payload: LoginRequest):
    user = get_user_by_email(payload.email)
    
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
