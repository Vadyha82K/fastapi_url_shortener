__all__ = ("router",)

from .detail_views import router as detail_router
from .list_views import router

router.include_router(detail_router)
