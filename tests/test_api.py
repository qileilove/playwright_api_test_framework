import pytest
from utils_tools.api_client import APIClient

BASE_URL = "https://your-api-endpoint.com"
HEADERS = {
    "Authorization": "Bearer YOUR_API_TOKEN"
}


@pytest.fixture(scope="module")
def api_client():
    client = APIClient(base_url=BASE_URL, headers=HEADERS)
    yield client
    client.close()


def test_get_request(api_client):
    response = api_client.get("/path/to/resource")
    assert response.status == 200
    response_body = response.json()
    assert "key" in response_body
    assert response_body["key"] == "expectedValue"


def test_post_request(api_client):
    response = api_client.post("/path/to/resource", {"key": "value"})
    assert response.status == 201
    response_body = response.json()
    assert "key" in response_body
    assert response_body["key"] == "expectedValue"


def test_put_request(api_client):
    response = api_client.put("/path/to/resource/1", {"key": "newValue"})
    assert response.status == 200
    response_body = response.json()
    assert "key" in response_body
    assert response_body["key"] == "newValue"


def test_delete_request(api_client):
    response = api_client.delete("/path/to/resource/1")
    assert response.status == 204
