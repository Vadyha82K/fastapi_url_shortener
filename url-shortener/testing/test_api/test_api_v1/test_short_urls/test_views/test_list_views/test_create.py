import random
import string
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
)
from testing.conftest import build_short_url_create_random_slug


def test_create_short_url(auth_client: TestClient) -> None:
    url = app.url_path_for("create_short_url")
    short_url_create = ShortUrlCreate(
        slug="".join(
            random.choices(string.ascii_letters, k=10),  # noqa: S311
        ),
        description="A short url",
        target_url="https://example.com",
    )
    data: dict[str, str] = short_url_create.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_values = ShortUrlCreate(**response_data)
    assert received_values == short_url_create, response_data


def test_create_short_url_already_exists(
    auth_client: TestClient,
    short_url: ShortUrl,
) -> None:
    short_url_create = ShortUrlCreate(**short_url.model_dump())
    data = short_url_create.model_dump(mode="json")
    url = app.url_path_for("create_short_url")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Short URL with by slug={short_url.slug!r} already exists"
    assert response_data["detail"] == expected_error_detail, response_data


class TestCreateInvalid:

    @pytest.fixture(
        params=[
            pytest.param(("a", "string_to_short"), id="to-short"),
            pytest.param(("foo-bar-spam-eggs", "string_to_long"), id="too-long"),
        ],
    )
    def short_url_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, Any], str]:
        build = build_short_url_create_random_slug()
        data = build.model_dump(mode="json")
        slug, err_type = request.param
        data["slug"] = slug
        return data, err_type

    def test_invalid_slug(
        self,
        short_url_create_values: tuple[dict[str, Any], str],
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("create_short_url")
        create_data, expected_error_type = short_url_create_values
        response = auth_client.post(
            url=url,
            json=create_data,
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == expected_error_type, error_detail
