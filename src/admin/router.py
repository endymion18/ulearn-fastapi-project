from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.admin.exceptions import WrongUserData
from src.admin.schemas import ChangeMainPage, ChangeStatsPage
from src.admin.utils import encode_jwt_token, verify_user, get_current_user, change_main_page_values, \
    restore_pages_to_default, change_stats_pages
from src.database import get_async_session
from src.models.models import User

admin_router = APIRouter(prefix="", tags=["Admin"])


@admin_router.post("/admin/main-page")
async def change_main_page(change_data: ChangeMainPage, admin: User = Depends(get_current_user),
                           session: AsyncSession = Depends(get_async_session)):
    await change_main_page_values(change_data, session)
    return "Main page changed successfully"


@admin_router.post("/admin/relevance-page")
async def change_relevance_page(change_data: ChangeStatsPage, admin: User = Depends(get_current_user),
                                session: AsyncSession = Depends(get_async_session)):
    await change_stats_pages('relevance', change_data, session)
    return "Relevance page changed successfully"


@admin_router.post("/admin/geography-page")
async def change_geography_page(change_data: ChangeStatsPage, admin: User = Depends(get_current_user),
                                session: AsyncSession = Depends(get_async_session)):
    await change_stats_pages('geography', change_data, session)
    return "Geography page changed successfully"


@admin_router.post("/admin/skills-page")
async def change_skills_page(change_data: ChangeStatsPage, admin: User = Depends(get_current_user),
                             session: AsyncSession = Depends(get_async_session)):
    await change_stats_pages('skills', change_data, session)
    return "Skills page changed successfully"


@admin_router.delete("/admin/pages")
async def restore_pages_values(admin: User = Depends(get_current_user),
                               session: AsyncSession = Depends(get_async_session)):
    await restore_pages_to_default(session)
    return "Pages restored to default"


@admin_router.post("/login")
async def login(user_data: OAuth2PasswordRequestForm = Depends(),
                session: AsyncSession = Depends(get_async_session)):
    name, password = user_data.username, user_data.password

    try:
        await verify_user(name, password, session)
    except WrongUserData as error:
        print(error.__str__())
        return JSONResponse(content={"detail": error.__str__()}, status_code=400)

    jwt_token = await encode_jwt_token({"sub": name})
    return {"access_token": jwt_token,
            "token_type": "bearer"}
