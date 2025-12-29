import pytest


def test_get_items_by_seller_success(base_url, http, created_item):
    seller_id = created_item["sellerId"]
    item_id = created_item["id"]

    url = f"{base_url}/api/1/{seller_id}/item"
    r = http.get(url)
    assert r.status_code == 200, f"GET {url} failed: {r.status_code} {r.text}"

    data = r.json()
    assert isinstance(data, list), f"Expected list, got: {data!r}"
    assert data, f"Expected non-empty list for seller {seller_id}, got: {data!r}"

    for x in data:
        assert isinstance(x, dict), f"Expected list[dict], got element: {x!r}"
        assert x.get("id"), f"Missing id in element: {x!r}"
        assert x.get("sellerId") == seller_id, f"Wrong sellerId in element: {x!r}"

    assert any(x.get("id") == item_id for x in data), (
        f"Created item id={item_id} not found in seller items. "
        f"seller_id={seller_id}, returned_ids={[x.get('id') for x in data if isinstance(x, dict)]}"
    )


@pytest.mark.parametrize(
    "bad_seller_id",
    [
        pytest.param("abc", id="letters"),
        pytest.param("12ab", id="mixed"),
    ],
)
def test_get_items_by_seller_bad_sellerid_400(base_url, http, bad_seller_id):
    url = f"{base_url}/api/1/{bad_seller_id}/item"
    r = http.get(url)
    assert r.status_code == 400, f"GET {url} expected 400, got {r.status_code}: {r.text}"
