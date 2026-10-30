from fastapi import APIRouter, Depends, HTTPException, Query, status
from database import get_db
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Annotated
from models import Client
from schemas.clients import CreateClient, ReadClient
from security import hash_password


router = APIRouter(prefix="/clients", tags=["clients"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post(
    "", 
    response_model=ReadClient, 
    status_code=status.HTTP_201_CREATED, 
    responses={409: {"description": "Email already exists"}}
)
def create_client(payload: CreateClient, db: db_dependency):
    client = Client(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name
    )
    db.add(client)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(client)
    return client