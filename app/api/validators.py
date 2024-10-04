# -*- coding: utf-8 -*-
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase


async def check_name_duplicate(
        name: str,
        model_crud: CRUDBase,
        session: AsyncSession,
) -> None:
    obj_id = await model_crud.get_id_by_name(name, session)
    if obj_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Объект с таким названием уже существует!',
        )


async def check_obj_exists(
        obj_id: int,
        model_crud: CRUDBase,
        session: AsyncSession,
) -> None:
    obj = await model_crud.get(obj_id, session)
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail='Объект не найден!'
        )

    return obj
