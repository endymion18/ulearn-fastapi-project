from starlette.requests import Request
from starlette.templating import Jinja2Templates
from fastapi import APIRouter

templates = Jinja2Templates(directory="../frontend/templates")

pages_router = APIRouter()


@pages_router.get("/")
async def get_base_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@pages_router.get("/relevance")
async def get_base_page(request: Request):
    return templates.TemplateResponse(request=request, name="sample.html")


@pages_router.get("/geography")
async def get_base_page(request: Request):
    return templates.TemplateResponse(request=request, name="sample.html")


@pages_router.get("/skills")
async def get_base_page(request: Request):
    return templates.TemplateResponse(request=request, name="sample.html")


@pages_router.get("/last-vacancies")
async def get_base_page(request: Request):
    return templates.TemplateResponse(request=request, name="sample.html")

