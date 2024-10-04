from fastapi import APIRouter

from app.api.endpoints import kitten_router, breed_router, user_router

main_router = APIRouter()
main_router.include_router(
    kitten_router,
    prefix='/kittens',
    tags=['Kittens']
)
main_router.include_router(
    breed_router,
    prefix='/breeds',
    tags=['Breeds']
)
main_router.include_router(user_router)
