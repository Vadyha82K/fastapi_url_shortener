import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    status,
    Request,
    Depends,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)

from core.config import (
    USERS_DB,
    REDIS_TOKENS_SET_NAME,
)
from .crud import storage
from .my_redis import redis_tokens
from schemas.short_url import ShortUrl


log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)

static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from developer portal. [Read more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic auth",
    description="Basic username + password",
    auto_error=False,
)


def prefetch_short_url(slug: str) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"URL {slug!r} not found",
    )


def save_storage_state(background_tasks: BackgroundTasks, request: Request):
    # Сначала код до входа внутрь view функции
    yield
    # Код после покидания view функции
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage")
        background_tasks.add_task(storage.save_state)


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
):
    if redis_tokens.sismember(
        REDIS_TOKENS_SET_NAME,
        api_token.credentials,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def validate_basic_auth(
    credentials: HTTPBasicCredentials,
):
    if (
        credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User credentials required. Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ],
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ],
):
    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        return validate_basic_auth(credentials=credentials)

    if api_token:
        return validate_api_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or basic auth required",
    )
