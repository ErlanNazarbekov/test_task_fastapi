from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Kitten


class CRUDKitten(CRUDBase):
    async def get_multi_by_breed_id(
            self,
            breed_id: int,
            session: AsyncSession,
    ):
        db_objs = await session.execute(
            select(self.model).where(self.model.breed_id == breed_id)
        )
        return db_objs.scalars().all()


kitten_crud = CRUDKitten(Kitten)
