import pytest
from fastapi import status
from fastapi.testclient import TestClient


def test_root_view(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    expected_message = "Hello World!"
    assert response_data["message"] == expected_message, response_data


@pytest.mark.parametrize(
    "name",
    [
        "Vadim",
        "",
        "Petr Ivanov",
        "Alex!#%",
    ],
)
def test_root_view_custom_name(
    name: str,
    client: TestClient,
) -> None:
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    expected_message = f"Hello {name}!"
    assert response_data["message"] == expected_message, response_data
