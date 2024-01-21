from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Depends

from src.database import get_async_session
from src.pages.utils import get_page_values

templates = Jinja2Templates(directory="../frontend/templates")

pages_router = APIRouter()


@pages_router.get("/")
async def get_base_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    page_values = await get_page_values(session)
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "vacancy_name": page_values.vacancy_name,
                                                     "first_paragraph": page_values.first_paragraph,
                                                     "second_paragraph_name": page_values.second_paragraph_name,
                                                     "second_paragraph": page_values.second_paragraph})


@pages_router.get("/relevance")
async def get_base_page(request: Request):
    return templates.TemplateResponse(request=request, name="relevance.html")


@pages_router.get("/geography")
async def get_base_page(request: Request):
    return templates.TemplateResponse(request=request, name="geography.html")


@pages_router.get("/skills")
async def get_base_page(request: Request):
    return templates.TemplateResponse(request=request, name="skills.html")


@pages_router.get("/last-vacancies")
async def get_base_page(request: Request):
    return templates.TemplateResponse(request=request, name="last-vacancies.html")

