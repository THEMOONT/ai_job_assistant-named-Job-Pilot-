from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.models.user import User

router = APIRouter()

class SignupData(BaseModel):
    full_name: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(data: SignupData):

    db = SessionLocal()

    existing = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        full_name=data.full_name,
        email=data.email,
        password=data.password
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {
        "message": "Account created",
        "user_id": user.id
    }


@router.post("/login")
def login(data: LoginData):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == data.email,
        User.password == data.password
    ).first()

    db.close()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "message": "Login success",
        "user_id": user.id,
        "full_name": user.full_name
    }
