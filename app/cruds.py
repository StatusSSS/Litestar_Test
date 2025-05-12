from typing import Sequence

import msgspec
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.exceptions import HTTPException

from app.models import User


class CRUDUser:
    @staticmethod
    def _not_found() -> HTTPException:  # tiny shortcut
        return HTTPException(status_code=404, detail="User not found")


    @staticmethod
    async def create(session: AsyncSession, data) -> User:
        user = User(**msgspec.structs.asdict(data))
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


    @staticmethod
    async def get(session: AsyncSession, user_id: int) -> User:
        user = await session.get(User, user_id)
        if user is None:
            raise CRUDUser._not_found()
        return user

    @staticmethod
    async def list(
        session: AsyncSession, *, offset: int = 0, limit: int = 20
    ) -> Sequence[User]:
        res = await session.execute(select(User).offset(offset).limit(limit))
        return res.scalars().all()


    @staticmethod
    async def update(session: AsyncSession, user_id: int, data) -> User:
        user = await CRUDUser.get(session, user_id)
        for field, value in msgspec.structs.asdict(data).items():
            if value is not None:
                setattr(user, field, value)
        await session.commit()
        await session.refresh(user)
        return user


    @staticmethod
    async def delete(session: AsyncSession, user_id: int) -> None:
        user = await CRUDUser.get(session, user_id)
        await session.delete(user)
        await session.commit()