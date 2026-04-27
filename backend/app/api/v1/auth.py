from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.models.user import User
from app.core.logger import auth_logger, error_logger
import bcrypt
import jwt
import datetime

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = "jobpilot_secret_key_change_in_production"
ALGORITHM = "HS256"


class SignupData(BaseModel):
    full_name: str
    email: str
    password: str


class LoginData(BaseModel):
    email: str
    password: str


def create_token(user_id: int, email: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        auth_logger.warning("Expired token used")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        auth_logger.warning("Invalid token used")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/signup")
def signup(data: SignupData):
    auth_logger.info(f"Signup attempt for email: {data.email}")
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            auth_logger.warning(f"Signup failed - email already exists: {data.email}")
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed = bcrypt.hashpw(
            data.password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        user = User(full_name=data.full_name, email=data.email, password=hashed)
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_token(user.id, user.email)
        auth_logger.info(f"Signup successful - user_id: {user.id}, email: {user.email}")

        return {"message": "Account created", "user_id": user.id, "token": token}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        error_logger.error(f"Signup error for {data.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Signup failed")
    finally:
        db.close()


@router.post("/login")
def login(data: LoginData):
    auth_logger.info(f"Login attempt for email: {data.email}")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == data.email).first()

        if not user:
            auth_logger.warning(f"Login failed - user not found: {data.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        valid = bcrypt.checkpw(
            data.password.encode("utf-8"),
            user.password.encode("utf-8")
        )

        if not valid:
            auth_logger.warning(f"Login failed - wrong password for: {data.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_token(user.id, user.email)
        auth_logger.info(f"Login successful - user_id: {user.id}, email: {user.email}")

        return {
            "message": "Login success",
            "user_id": user.id,
            "full_name": user.full_name,
            "token": token
        }

    except HTTPException:
        raise
    except Exception as e:
        error_logger.error(f"Login error for {data.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")
    finally:
        db.close()


@router.get("/me")
def get_me(token_data: dict = Depends(verify_token)):
    auth_logger.info(f"Profile fetched for user_id: {token_data['user_id']}")
    return {"user_id": token_data["user_id"], "email": token_data["email"]}
