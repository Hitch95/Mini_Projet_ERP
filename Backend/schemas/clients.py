from pydantic import BaseModel, Field, ConfigDict, field_validator


class CreateClient(BaseModel):
    email: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=1, max_length=50)
    first_name: str = Field(min_length=1, max_length=30)
    last_name: str = Field(min_length=1, max_length=30)
    
class UpdateClient(BaseModel):
    email: str | None = Field(default=None, min_length=1, max_length=30)
    password: str | None = Field(default=None, min_length=1, max_length=50)
    first_name: str | None = Field(default=None, min_length=1, max_length=30)
    last_name: str | None = Field(default=None, min_length=1, max_length=30)

    # un champ absent du PATCH reste à None, mais un null explicite doit être refusé
    @field_validator("email", "password", "first_name", "last_name")
    @classmethod
    def reject_explicit_null(cls, value):
        if value is None:
            raise ValueError("ne peut pas être null")
        return value
    
class ReadClient(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    
    # from_attributes=True permet à Pydantic de construire la réponse depuis un objet SQLAlchemy
    model_config = ConfigDict(from_attributes=True)