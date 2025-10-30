from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from database import get_db, Base, engine
import models, schemas

SECRET_KEY = "replace-this-with-a-strong-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
def register(req: schemas.RegisterRequest, db: Session = Depends(get_db)):
    # create org
    org = models.Organization(name=req.organization_name or "My Organization")
    db.add(org); db.flush()
    # create user
    hashed = pwd_context.hash(req.password)
    user = models.User(email=req.email, password_hash=hashed, full_name=req.full_name, organization_id=org.id, role="owner")
    db.add(user); db.commit()
    return {"message": "User registered", "organization_id": org.id}

@router.post("/login")
def login(req: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not pwd_context.verify(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user.email, "uid": user.id, "org": user.organization_id})
    return {"access_token": token, "token_type": "bearer"}
