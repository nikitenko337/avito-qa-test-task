import uuid

import pytest


def test_get_statistic_by_id_success(base_url, http, created_item_id):
    url = f"{base_url}/api/1/statistic/{created_item_id}"
    r = http.get(url)
    assert r.status_code == 200, f"GET {url} failed: {r.status_code} {r.text}"

    data = r.json()
    assert isinstance(data, list), f"Expected list, got: {data!r}"
    assert data, f"Expected non-empty list, got: {data!r}"

    obj = data[0]
    assert isinstance(obj.get("likes"), int)
    assert isinstance(obj.get("viewCount"), int)
    assert isinstance(obj.get("contacts"), int)


@pytest.mark.parametrize(
    "bad_id",
    [
        pytest.param("no-such-id-123456", id="not_uuid_1"),
        pytest.param("not-a-uuid", id="not_uuid_2"),
    ],
)
def test_get_statistic_invalid_id_400(base_url, http, bad_id):
    url = f"{base_url}/api/1/statistic/{bad_id}"
    r = http.get(url)
    assert r.status_code == 400, f"GET {url} expected 400, got {r.status_code}: {r.text}"


def test_get_statistic_not_found_valid_uuid(base_url, http):
    missing_id = str(uuid.uuid4())
    url = f"{base_url}/api/1/statistic/{missing_id}"
    r = http.get(url)

    assert r.status_code in (404, 200), f"Unexpected status for {url}: {r.status_code} {r.text}"
    if r.status_code == 200:
        data = r.json()
        assert data in ([], {}), f"Expected empty body for not found, got: {data!r}"
