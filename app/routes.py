from typing import Sequence, List

from litestar import Controller, delete, get, post, put
from litestar.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import msgspec

from .models import User
from .schemas import UserCreate, UserRead, UserUpdate


def _to_read(u: User) -> UserRead:
    return UserRead(
        id=u.id,
        name=u.name,
        surname=u.surname,
        created_at=u.created_at,
        updated_at=u.updated_at,
    )


class UserController(Controller):
    path = "/users"

    @post(summary="Создать пользователя", status_code=201)
    async def create_user(
        self,
        data: UserCreate,
        session: AsyncSession,
    ) -> UserRead:
        user = User(**msgspec.structs.asdict(data))
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return _to_read(user)

    @get(summary="Список пользователей")
    async def list_users(self, session: AsyncSession) -> Sequence[UserRead]:
        res = await session.execute(select(User))
        return [_to_read(u) for u in res.scalars().all()]

    @get(path="/{user_id:int}", summary="Получить пользователя")
    async def get_user(self, user_id: int, session: AsyncSession) -> UserRead:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return _to_read(user)

    @put(path="/{user_id:int}", summary="Обновить пользователя")
    async def update_user(
        self,
        user_id: int,
        data: UserUpdate,
        session: AsyncSession,
    ) -> UserRead:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for field, value in msgspec.structs.asdict(data).items():
            setattr(user, field, value)

        await session.commit()
        await session.refresh(user)
        return _to_read(user)

    @delete(path="/{user_id:int}", summary="Удалить пользователя", status_code=204)
    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
        await session.commit()
