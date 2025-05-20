import logging

from pydantic import (
    BaseModel,
    ValidationError,
)
from redis import Redis

from core import config
from core.config import SHORT_URLS_STORAGE_FILEPATH
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlPartialUpdate,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.Redis_DB_SHORT_URLS,
    decode_responses=True,
)


class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        SHORT_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Saved short urls to storage file.")

    @classmethod
    def from_state(cls) -> "ShortUrlsStorage":
        if not SHORT_URLS_STORAGE_FILEPATH.exists():
            log.info("Short urls file doesn't not exist.")
            return ShortUrlsStorage()
        return cls.model_validate_json(SHORT_URLS_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = ShortUrlsStorage.from_state()
            log.warning("Recovered data from storage file.")
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error.")
            return
        # обновляем свойство напрямую
        # если будут новые свойства,
        # то их тоже надо обновить
        self.slug_to_short_url.update(
            data.slug_to_short_url,
        )

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(
            **short_url_in.model_dump(),
        )
        redis.hset(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )
        log.info("Created short url %s", short_url)
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        result = self.slug_to_short_url.pop(slug, None)
        log.info("Delete short url %s", result)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self.slug_to_short_url[short_url.slug] = short_url
        log.info("Update short url %s", short_url)
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlPartialUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, value)
        self.slug_to_short_url[short_url.slug] = short_url
        log.info("Update partial short url %s", short_url)
        return short_url


storage = ShortUrlsStorage()
