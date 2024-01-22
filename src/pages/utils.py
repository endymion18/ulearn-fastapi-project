from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import MainPage, RelevancePage, GeographyPage, SkillsPage


async def get_base_page_values(session: AsyncSession) -> MainPage:
    page_values = await session.execute(select(MainPage).where(MainPage.value == 'new'))
    if page_values.scalar() is None:
        page_values = await session.execute(select(MainPage).where(MainPage.value == 'default'))

    return page_values.scalar()


async def get_graphics_and_tables(table_name: str,
                                  session: AsyncSession):
    match table_name:
        case 'geography':
            table = GeographyPage
        case 'relevance':
            table = RelevancePage
        case 'skills':
            table = SkillsPage
        case default:
            table = None

    page_values = await session.execute(select(table).where(table.value == 'new'))
    if page_values.scalar() is None:
        page_values = await session.execute(select(table).where(table.value == 'default'))

    table_data = page_values.scalar().table_data['data']

    return table_data
