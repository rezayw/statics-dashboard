from fastapi import APIRouter, HTTPException, Depends, Form
from app.crud.user import get_user_by_email, create_user, verify_password
from app.auth.jwt_handler import create_access_token

router = APIRouter()

@router.post("/register")
def register(email: str = Form(...), full_name: str = Form(...), password: str = Form(...)):
    if get_user_by_email(email):
        raise HTTPException(status_code=400, detail="Email already registered")
    create_user(email, full_name, password)
    return {"msg": "User created"}

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
