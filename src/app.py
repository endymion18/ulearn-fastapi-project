from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from pages.router import pages_router

app = FastAPI(
    title="Ulearn FastAPI Project"
)

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

app.include_router(pages_router)
