from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from database import get_db
import models, schemas

ALGORITHM = "HS256"
SECRET_KEY = "replace-this-with-a-strong-secret"

router = APIRouter()

def get_token_payload(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("", response_model=list[schemas.CustomerOut])
def list_customers(db: Session = Depends(get_db), payload: dict = Depends(get_token_payload)):
    org_id = payload.get("org")
    rows = db.query(models.Customer).filter(models.Customer.organization_id == org_id).all()
    return rows

@router.post("", response_model=schemas.CustomerOut)
def create_customer(data: schemas.CustomerCreate, db: Session = Depends(get_db), payload: dict = Depends(get_token_payload)):
    org_id = payload.get("org")
    row = models.Customer(organization_id=org_id, name=data.name, email=data.email, phone=data.phone)
    db.add(row); db.commit(); db.refresh(row)
    return row
