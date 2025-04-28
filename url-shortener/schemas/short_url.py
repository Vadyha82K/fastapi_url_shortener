from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, AnyHttpUrl


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: Annotated[
        str,
        MaxLen(200),
    ] = ""


class ShortUrlCreate(ShortUrlBase):
    """
    Модель создания сокращенной ссылки
    """

    slug: Annotated[
        str,
        MinLen(3),
        MaxLen(10),
    ]


class ShortUrlUpdate(ShortUrlBase):
    """
    Модель обновления информации о сокращенной ссылке
    """

    description: Annotated[
        str,
        MaxLen(200),
    ]


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенной ссылки
    """

    slug: str
