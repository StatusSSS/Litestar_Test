from __future__ import annotations

from datetime import datetime
import msgspec


class UserBase(msgspec.Struct):
    name: str
    surname: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(msgspec.Struct, kw_only=True, omit_defaults=True):
    name: str | None = None
    surname: str | None = None
    password: str | None = None
