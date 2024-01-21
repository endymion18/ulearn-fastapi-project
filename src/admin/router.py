from fastapi import APIRouter

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.get("")
async def get_admin_page():
    return "not working yet"
