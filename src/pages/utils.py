from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import MainPage


async def get_page_values(session: AsyncSession) -> MainPage:
    page_values = await session.execute(select(MainPage).where(MainPage.value == 'new'))
    if page_values.scalar() is None:
        page_values = await session.execute(select(MainPage).where(MainPage.value == 'default'))

    return page_values.scalar()

