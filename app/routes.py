from typing import Sequence

from litestar import Controller, delete, get, post, put
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated
from litestar.params import Parameter

from app.schemas import UserCreate, UserRead, UserUpdate, PaginatedUserResponse
from app.cruds import CRUDUser


def _to_read(model) -> UserRead:
    return UserRead(
        id=model.id,
        name=model.name,
        surname=model.surname,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class UserController(Controller):
    path = "/api/v1/users"
    tags = ["Users"]


    @post(summary="Создать пользователя", status_code=201)
    async def create_user(self, data: UserCreate, session: AsyncSession) -> UserRead:
        user = await CRUDUser.create(session, data)
        return _to_read(user)

    @get(summary="Список пользователей")
    async def list_users(
            self,
            session: AsyncSession,
            page: Annotated[int, Parameter(query="page", ge=1)] = 1,
            page_size: Annotated[int, Parameter(query="page_size", ge=1, le=100)] = 20,
    ) -> PaginatedUserResponse:
        offset = (page - 1) * page_size
        users = await CRUDUser.list(session, offset=offset, limit=page_size)

        total = await CRUDUser.count(session)

        return PaginatedUserResponse(
            page=page,
            limit=page_size,
            count=total,
            users=[_to_read(u) for u in users],
        )


    @get(path="/{user_id:int}", summary="Получить пользователя")
    async def get_user(self, user_id: int, session: AsyncSession) -> UserRead:
        user = await CRUDUser.get(session, user_id)
        return _to_read(user)


    @put(path="/{user_id:int}", summary="Обновить пользователя")
    async def update_user(
        self, user_id: int, data: UserUpdate, session: AsyncSession
    ) -> UserRead:
        user = await CRUDUser.update(session, user_id, data)
        return _to_read(user)


    @delete(path="/{user_id:int}", summary="Удалить пользователя", status_code=204)
    async def delete_user(self, user_id: int, session: AsyncSession) -> None:
        await CRUDUser.delete(session, user_id)