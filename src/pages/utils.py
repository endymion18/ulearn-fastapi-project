from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import MainPage, RelevancePage


async def get_base_page_values(session: AsyncSession) -> MainPage:
    page_values = await session.execute(select(MainPage).where(MainPage.value == 'new'))
    if page_values.scalar() is None:
        page_values = await session.execute(select(MainPage).where(MainPage.value == 'default'))

    return page_values.scalar()


async def get_relevance_page_values(session: AsyncSession) -> RelevancePage:
    page_values = await session.execute(select(RelevancePage).where(RelevancePage.value == 'new'))
    if page_values.scalar() is None:
        page_values = await session.execute(select(RelevancePage).where(RelevancePage.value == 'default'))

    table_data = page_values.scalar().table_data['data']

    return table_data

