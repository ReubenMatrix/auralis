from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.repository.db import get_db_connection 

router = APIRouter()

@router.get("/hello")
def hello():
    return {"message": "Hello from routes 👋"}


@router.get("/health")
def health(db: Session = Depends(get_db_connection)):
    return {"status": "db connected"}