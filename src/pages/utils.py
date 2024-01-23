import re
from datetime import datetime
from typing import Type

import requests
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import MainPage, RelevancePage, GeographyPage, SkillsPage, CurrentVacancy


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


async def get_current_vacancy_name(session: AsyncSession):
    vacancy_name = await session.execute(select(CurrentVacancy.vacancy_name).where(CurrentVacancy.value == 'new'))
    if vacancy_name.scalar() is None:
        vacancy_name = await session.execute(
            select(CurrentVacancy.vacancy_name).where(CurrentVacancy.value == 'default'))

    return vacancy_name.scalar()


async def get_last_vacancies(session: AsyncSession):
    vacancy_name = await get_current_vacancy_name(session)
    request = requests.get(f"https://api.hh.ru/vacancies?text={vacancy_name}&order_by=publication_time&per_page=10")

    if request.status_code == 200:
        vacancies_data = []
        vacancies = request.json()["items"]
        for vacancy in vacancies:
            if vacancy["salary"] is None:
                salary = "Не указано"
            else:
                if vacancy["salary"]["from"] is None:
                    salary_from = ""
                else:
                    salary_from = f'от {vacancy["salary"]["from"]}'

                if vacancy["salary"]["to"] is None:
                    salary_to = ""
                else:
                    salary_to = f'до {vacancy["salary"]["to"]}'

                salary = f'{salary_from} {salary_to} {vacancy["salary"]["currency"]}'
            published_at = str(datetime.strptime(vacancy["published_at"], "%Y-%m-%dT%H:%M:%S%z").astimezone())
            published_at = re.sub(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\+(\d{2}):(\d{2})',
                                  r'\3.\2.\1 \4:\5', published_at)
            vacancies_data.append({
                "name": vacancy["name"],
                "company": vacancy["employer"]["name"],
                "salary": salary,
                "area_name": vacancy["area"]["name"],
                "published_at": published_at
            })

        return vacancies_data
    else:
        return None
