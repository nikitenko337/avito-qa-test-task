import copy
import uuid
import pytest

def test_create_item_success(base_url, http, seller_id):
    url = f"{base_url}/api/1/item"
    payload = {
        "sellerID": seller_id,
        "name": "Test item QA create success",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }

    r = http.post(url, json=payload)
    assert r.status_code == 200, f"POST {url} failed: {r.status_code} {r.text}"

    data = r.json()
    assert isinstance(data, dict), f"Expected dict JSON, got: {data!r}"

    # API может вернуть {"id": "<uuid>"} или {"status": "Сохранили объявление - <uuid>"}
    item_id = data.get("id")
    if not item_id:
        status = data.get("status")
        assert isinstance(status, str) and status, f"Expected 'id' or 'status' in response: {data!r}"
        item_id = status.split()[-1]

    uuid.UUID(str(item_id))


@pytest.mark.parametrize(
    "mutator",
    [
        pytest.param(lambda p: p.pop("sellerID", None), id="missing_sellerID"),
        pytest.param(lambda p: p.__setitem__("price", "1000"), id="price_wrong_type"),
    ],
)
def test_create_item_validation_errors_400(base_url, http, seller_id, mutator):
    url = f"{base_url}/api/1/item"
    payload = {
        "sellerID": seller_id,
        "name": "Test item QA validation",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }

    payload2 = copy.deepcopy(payload)
    mutator(payload2)

    r = http.post(url, json=payload2)
    assert r.status_code == 400, f"POST {url} expected 400, got {r.status_code}: {r.text}"
