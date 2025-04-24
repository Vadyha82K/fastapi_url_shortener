from pydantic import AnyHttpUrl

from schemas.short_url import ShortUrl

SHORT_URLS = [
    ShortUrl(
        target_url=AnyHttpUrl("https://www.example.com"),
        slug="example",
    ),
    ShortUrl(
        target_url=AnyHttpUrl("https://www.google.com"),
        slug="search",
    ),
]
