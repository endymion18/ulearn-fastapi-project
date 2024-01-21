from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Depends

from src.database import get_async_session
from src.pages.utils import get_base_page_values, get_relevance_page_values

templates = Jinja2Templates(directory="../frontend/templates")

pages_router = APIRouter()


@pages_router.get("/")
async def get_base_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    base_page_values = await get_base_page_values(session)
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "vacancy_name": base_page_values.vacancy_name,
                                                     "first_paragraph": base_page_values.first_paragraph,
                                                     "second_paragraph_name": base_page_values.second_paragraph_name,
                                                     "second_paragraph": base_page_values.second_paragraph})


@pages_router.get("/relevance")
async def get_relevance_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    relevance_page_values = await get_relevance_page_values(session)
    return templates.TemplateResponse("relevance.html", {"request": request,
                                                         "table_data": relevance_page_values})


@pages_router.get("/geography")
async def get_relevance_page(request: Request):
    return templates.TemplateResponse(request=request, name="geography.html")


@pages_router.get("/skills")
async def get_skills_page(request: Request):
    return templates.TemplateResponse(request=request, name="skills.html")


@pages_router.get("/last-vacancies")
async def get_last_vacancies_page(request: Request):
    return templates.TemplateResponse(request=request, name="last-vacancies.html")
