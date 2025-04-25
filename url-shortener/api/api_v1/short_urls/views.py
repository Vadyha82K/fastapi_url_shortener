from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)

from .dependencies import (
    prefetch_short_url,
)
from .crud import storage
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
)

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
)


@router.get(
    "/",
    response_model=list[ShortUrl],
)
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
) -> ShortUrl:

    return storage.create(short_url_create)


@router.get(
    "/{slug}/",
    response_model=ShortUrl,
)
def read_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
):
    return url
