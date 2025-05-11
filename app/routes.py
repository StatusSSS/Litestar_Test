from typing import Sequence

from litestar import Controller, delete, get, post, put
from litestar.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from .models import User
from .schemas import UserCreate, UserRead, UserUpdate


class UserController(Controller):
    path = "/users"

    @post(summary="Создать пользователя", status_code=201)
    async def create_user(
        self,
        data: UserCreate,
        session: AsyncSession,
    ) -> UserRead:
        user = User(**data.model_dump())

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return UserRead.model_validate(user, from_attributes=True)

    @get(summary="Список пользователей")
    async def list_users(
        self,
        session: AsyncSession,
    ) -> Sequence[UserRead]:
        res = await session.execute(select(User))
        return [
            UserRead.model_validate(u, from_attributes=True)
            for u in res.scalars().all()
        ]

    @get(path="/{user_id:int}", summary="Получить пользователя")
    async def get_user(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> UserRead:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserRead.model_validate(user, from_attributes=True)

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

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        await session.commit()
        await session.refresh(user)
        return UserRead.model_validate(user, from_attributes=True)

    @delete(path="/{user_id:int}", summary="Удалить пользователя", status_code=204)
    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(user)
        await session.commit()

