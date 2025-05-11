import logging
from fastapi import (
    HTTPException,
    BackgroundTasks,
)
from starlette import status

from .crud import storage
from schemas.short_url import ShortUrl


log = logging.getLogger(__name__)


def prefetch_short_url(slug: str) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


def save_storage_state(
    background_tasks: BackgroundTasks,
):
    # Сначала код до входа внутрь view функции
    yield
    # Код после покидания view функции
    log.info("Add background task to save storage")
    background_tasks.add_task(storage.save_state)
