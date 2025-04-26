__all__ = ("router",)

from .list_views import router
from .detail_views import router as detail_router


router.include_router(detail_router)
