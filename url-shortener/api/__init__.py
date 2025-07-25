from fastapi import APIRouter

from .api_v1 import router as api_v1_router

router = APIRouter(
    prefix="/auth",
)

router.include_router(api_v1_router)
