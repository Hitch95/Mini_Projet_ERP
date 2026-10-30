import os
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Annotated
from models import Client
from security import hash_password, verify_password
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime, timezone
import jwt
from jwt.exceptions import InvalidTokenError


router = APIRouter(prefix="/auth", tags=["auth"])

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Never hard-code the JWT signing key: provide it through the SECRET_KEY environment variable.
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
TOKEN_MINUTES = 60

# Checked when the email is unknown, so the response time does not reveal which emails exist.
DUMMY_HASH = hash_password("dummy-password")


def authenticate_client(email: str, password: str, db: Session) -> Client | None:
    client = db.scalars(select(Client).where(Client.email == email)).first()
    if client is None:
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, client.hashed_password):
        return None
    return client


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=TOKEN_MINUTES)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post(
    "/login",
    response_model=Token,
    responses={401: {"description": "Incorrect email or password"}},
)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    client = authenticate_client(form.username, form.password, db)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(client.id), token_type="bearer")


def get_current_client(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency) -> Client:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client_id = int(payload["sub"])
    except (InvalidTokenError, KeyError, ValueError):
        raise credentials_error
    # the role is read from the database, not from the token: a deleted account or a role change applies immediately
    client = db.get(Client, client_id)
    if client is None:
        raise credentials_error
    return client


def require_admin(client: Annotated[Client, Depends(get_current_client)]) -> Client:
    if client.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return client
