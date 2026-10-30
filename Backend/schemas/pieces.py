from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict, field_validator


class CreatePiece(BaseModel):
    reference: str = Field(min_length=1, max_length=8)
    name: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(default=0, ge=0)
    
class UpdatePiece(BaseModel):
    reference: str | None = Field(default=None, min_length=1, max_length=8)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)

    # un champ absent du PATCH reste à None, mais un null explicite doit être refusé
    @field_validator("reference", "name", "price", "stock")
    @classmethod
    def reject_explicit_null(cls, value):
        if value is None:
            raise ValueError("ne peut pas être null")
        return value
    
class ReadPiece(BaseModel):
    id: int
    reference: str
    name: str
    price: Decimal
    stock: int
    
    # from_attributes=True permet à Pydantic de construire la réponse depuis un objet SQLAlchemy
    model_config = ConfigDict(from_attributes=True)