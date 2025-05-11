from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(..., max_length=128)
    surname: str = Field(..., max_length=128)

    model_config = {
        "from_attributes": True,
    }


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=256)


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    name: str | None = Field(None, max_length=128)
    surname: str | None = Field(None, max_length=128)
    password: str | None = Field(default=None, min_length=6, max_length=256)

    model_config = {"from_attributes": True}
