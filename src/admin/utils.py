import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin.exceptions import WrongUserData
from src.admin.schemas import ChangeMainPage, ChangeStatsPage
from src.database import get_async_session
from src.models.models import User, MainPage, RelevancePage, SkillsPage, GeographyPage

secret_key = "veryveryreallysecretlongkey123123"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="Bearer")


async def encode_jwt_token(data: dict):
    jwt_token = jwt.encode(data, secret_key, "HS256")
    return jwt_token


async def verify_user(name: str, password: str, session: AsyncSession):
    user = await session.execute(select(User.name).where(User.name == name))
    if user.scalar() is None:
        raise WrongUserData("This user does not exist")

    password_db = await session.execute(select(User.password).where(User.password == password))
    if not password == password_db.scalar():
        raise WrongUserData("Password is incorrect")


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
    decoded_token = jwt.decode(token, secret_key, ["HS256"])
    name = decoded_token.get("sub")
    stmt = await session.execute(select(User).where(User.name == name))
    return stmt.scalar()


async def change_main_page_values(data: ChangeMainPage, session: AsyncSession):
    main_page_values = await session.execute(select(MainPage).where(MainPage.value == 'new'))
    if main_page_values.scalar() is None:
        await session.execute(insert(MainPage).values(
            value='new',
            vacancy_name=data.vacancy_name,
            first_paragraph=data.first_paragraph,
            second_paragraph_name=data.second_paragraph_name,
            second_paragraph=data.second_paragraph
        ))
    else:
        await session.execute(update(MainPage).where(MainPage.value == 'new').values(
            vacancy_name=data.vacancy_name,
            first_paragraph=data.first_paragraph,
            second_paragraph_name=data.second_paragraph_name,
            second_paragraph=data.second_paragraph
        ))

    await session.commit()


async def restore_pages_to_default(session: AsyncSession):
    await session.execute(delete(MainPage).where(MainPage.value == 'new'))
    await session.execute(delete(RelevancePage).where(RelevancePage.value == 'new'))
    await session.execute(delete(GeographyPage).where(GeographyPage.value == 'new'))
    await session.execute(delete(SkillsPage).where(SkillsPage.value == 'new'))

    await session.commit()


async def change_stats_pages(table_name: str, data: ChangeStatsPage, session: AsyncSession):
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
        await session.execute(insert(table).values(
            value='new',
            table_data=data.data
        ))
    else:
        await session.execute(update(table).where(table.value == 'new').values(
            table_data=data.data
        ))

    await session.commit()

