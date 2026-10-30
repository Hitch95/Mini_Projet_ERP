from fastapi import APIRouter, Depends, HTTPException, Query, status
from database import get_db
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Annotated
from models import Piece
from schemas.pieces import CreatePiece, UpdatePiece, ReadPiece


router = APIRouter(prefix="/pieces", tags=["pieces"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[ReadPiece])
def read_pieces(
    db: db_dependency,
    search: str | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    query = select(Piece).order_by(Piece.id)
    if search:
        pattern = f"%{search}%"
        query = query.where(or_(Piece.name.ilike(pattern), Piece.reference.ilike(pattern)))
    query = query.offset((page - 1) * limit).limit(limit)
    return db.scalars(query).all()


@router.get(
    "/{piece_id}",
    response_model=ReadPiece,
    responses={404: {"description": "Piece not found"}},
)
def read_piece(piece_id: int, db: db_dependency):
    piece = db.get(Piece, piece_id)
    if piece is None:
        raise HTTPException(status_code=404, detail="Piece not found")
    return piece


@router.post(
    "",
    response_model=ReadPiece,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Reference already exists"}},
)
def create_piece(payload: CreatePiece, db: db_dependency):
    piece = Piece(**payload.model_dump())
    db.add(piece)
    # le schéma bloque déjà prix et stock négatifs, donc l'erreur d'intégrité vient de la référence en doublon
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Reference already exists")
    db.refresh(piece)
    return piece


@router.patch(
    "/{piece_id}",
    response_model=ReadPiece,
    responses={
        404: {"description": "Piece not found"},
        409: {"description": "Reference already exists"},
    },
)
def update_piece(piece_id: int, payload: UpdatePiece, db: db_dependency):
    piece = db.get(Piece, piece_id)
    if piece is None:
        raise HTTPException(status_code=404, detail="Piece not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(piece, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Reference already exists")
    db.refresh(piece)
    return piece
