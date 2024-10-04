# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.kitten import kitten_crud
from app.crud.breed import breed_crud
from app.api.validators import check_name_duplicate, check_obj_exists
from app.schemas.kitten import (
    KittenCreate, KittenDB,
    KittenUpdate, KittenWithBreed
)
from app.models import Kitten, Breed
from app.core.user import current_superuser, current_user

router = APIRouter()


@router.post(
    '/',
    response_model=KittenDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_kitten(
        kitten: KittenCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(kitten.name, kitten_crud, session)
    new_kitten = await kitten_crud.create(kitten, session)

    return new_kitten


@router.get(
    '/',
    response_model=list[KittenDB],
    dependencies=[Depends(current_user)],
)
async def get_all_kittens(
        session: AsyncSession = Depends(get_async_session)
):
    all_kittens = await kitten_crud.get_multi(session)

    return all_kittens


@router.get(
    '/{kitten_id}',
    response_model=KittenDB,
    dependencies=[Depends(current_user)],
)
async def get_kitten(
        kitten_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    kitten = await check_obj_exists(kitten_id, kitten_crud, session)

    return kitten


@router.get(
    '/breed/{breed_id}',
    response_model=KittenWithBreed,
    dependencies=[Depends(current_user)],
)
async def get_kittens_by_breed(
        breed_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    breed = await check_obj_exists(breed_id, breed_crud, session)
    kittens = await kitten_crud.get_multi_by_breed_id(breed_id, session)

    return {
        'breed_name': breed.name,
        'kittens': kittens
    }


@router.patch(
    '/{kitten_id}',
    response_model=KittenDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_kitten(
        kitten_id: int,
        obj_in: KittenUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    kitten = await check_obj_exists(kitten_id, kitten_crud, session)
    kitten = await kitten_crud.update(kitten, obj_in, session)

    return kitten


@router.delete(
    '/{kitten_id}',
    response_model=KittenDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_kitten(
        kitten_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    kitten = await check_obj_exists(kitten_id, kitten_crud, session)
    kitten = await kitten_crud.delete(kitten, session)

    return kitten
