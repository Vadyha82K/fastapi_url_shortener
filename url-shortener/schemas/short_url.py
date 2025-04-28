from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, AnyHttpUrl


DescriptionString = Annotated[
    str,
    MaxLen(200),
]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: DescriptionString = ""


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

    description: DescriptionString


class ShortUrlPartialUpdate(BaseModel):
    """
    Модель для частичного обновления информации
    о сокращенной ссылке
    """

    target_url: AnyHttpUrl | None = None
    description: DescriptionString | None = None


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенной ссылки
    """

    slug: str
