import uuid

import pytest


def test_get_item_by_id_success(base_url, http, created_item_id):
    url = f"{base_url}/api/1/item/{created_item_id}"
    r = http.get(url)
    assert r.status_code == 200, f"GET {url} failed: {r.status_code} {r.text}"

    data = r.json()
    if isinstance(data, list):
        assert data, f"Expected non-empty list for existing id, got: {data!r}"
        obj = data[0]
    else:
        assert isinstance(data, dict), f"Expected dict or list[dict], got: {data!r}"
        obj = data

    assert obj["id"] == created_item_id
    assert "sellerId" in obj
    assert "name" in obj
    assert "price" in obj
    assert "statistics" in obj
    assert "createdAt" in obj


@pytest.mark.parametrize(
    "bad_id",
    [
        pytest.param("no-such-id-123456", id="not_uuid_1"),
        pytest.param("not-a-uuid", id="not_uuid_2"),
    ],
)
def test_get_item_by_id_invalid_id_400(base_url, http, bad_id):
    url = f"{base_url}/api/1/item/{bad_id}"
    r = http.get(url)
    assert r.status_code == 400, f"GET {url} expected 400, got {r.status_code}: {r.text}"


def test_get_item_by_id_not_found_valid_uuid(base_url, http):
    missing_id = str(uuid.uuid4())
    url = f"{base_url}/api/1/item/{missing_id}"
    r = http.get(url)

    assert r.status_code in (404, 200), f"Unexpected status for {url}: {r.status_code} {r.text}"
    if r.status_code == 200:
        data = r.json()
        assert data in ([], {}), f"Expected empty body for not found, got: {data!r}"
