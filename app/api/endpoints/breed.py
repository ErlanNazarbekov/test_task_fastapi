from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.breed import breed_crud
from app.api.validators import check_name_duplicate, check_obj_exists
from app.schemas.breed import BreedCreate, BreedDB
from app.models.breed import Breed
from app.core.user import current_superuser, current_user

router = APIRouter()


@router.post(
    '/',
    response_model=BreedDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_breed(
        breed: BreedCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(breed.name, breed_crud, session)
    new_breed = await breed_crud.create(breed, session)

    return new_breed


@router.get(
    '/',
    response_model=list[BreedDB],
    dependencies=[Depends(current_user)],
)
async def get_all_breeds(
        session: AsyncSession = Depends(get_async_session)
):
    all_breeds = await breed_crud.get_multi(session)

    return all_breeds


@router.delete(
    '/{breed_id}',
    response_model=BreedDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_breed(
        breed_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    breed = await check_obj_exists(breed_id, breed_crud, session)
    await breed_crud.delete(breed, session)

    return breed
