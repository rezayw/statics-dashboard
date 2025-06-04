from app.db.base import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(email: str):
    db = SessionLocal()
    return db.query(User).filter(User.email == email).first()

def create_user(email: str, full_name: str, password: str):
    db = SessionLocal()
    hashed_pw = pwd_context.hash(password)
    user = User(email=email, full_name=full_name, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)
