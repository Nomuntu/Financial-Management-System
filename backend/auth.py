# backend/auth.py
from datetime import datetime, timedelta
import os
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt

from database import get_db
import models
import schemas

router = APIRouter()

# ---- Password hashing (avoids bcrypt 72-byte limit) ----
# bcrypt_sha256 first SHA-256 hashes the password, then bcrypts the result.
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

# ---- JWT settings ----
SECRET_KEY = os.getenv("SECRET_KEY", "please-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(req: schemas.RegisterRequest, db: Session = Depends(get_db)):
    """
    Create organization + admin user.
    Body: { full_name, organization_name, email, password }
    """
    # Check if email already exists
    existing = db.query(models.User).filter(models.User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create org
    org = models.Organization(name=req.organization_name)
    db.add(org)
    db.flush()  # populate org.id

    # Hash password (bcrypt_sha256 -> no 72-byte limit)
    hashed = pwd_context.hash(req.password)

    # Create user (admin of this org)
    user = models.User(
        full_name=req.full_name,
        email=req.email,
        password_hash=hashed,
        organization_id=org.id,
        is_admin=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered", "organization_id": org.id, "user_id": user.id}


@router.post("/login")
def login(req: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email + password -> returns JWT access token.
    Body: { email, password }
    """
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not pwd_context.verify(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(
        {"sub": str(user.id), "org": str(user.organization_id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "organization_id": user.organization_id,
            "is_admin": user.is_admin,
        },
    }
