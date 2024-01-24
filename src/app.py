from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.pages.router import pages_router
from src.admin.router import admin_router

app = FastAPI(
    title="Ulearn FastAPI Project"
)

app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

app.include_router(pages_router)
app.include_router(admin_router)
