import os
import random
import re
import time
import uuid
from typing import Any, Dict

import pytest
import requests

UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}"
)

DEFAULT_TIMEOUT = 10  # секунды (чтобы тесты не висели, если стенду плохо)

def _base_url() -> str:
    return os.getenv("BASE_URL", "https://qa-internship.avito.com").rstrip("/")

def _unique_seller_id() -> int:
    # Генерация уникального sellerID в диапазоне 111111–999999 (возможны пересечения, так как стенд общий)
    seed = int(time.time() * 1000) % 1_000_000
    value = seed + random.randint(0, 9999)
    return 111111 + (value % (999999 - 111111 + 1))

def extract_item_id(resp_json: Any) -> str:
    if not isinstance(resp_json, dict):
        raise AssertionError(f"Expected dict JSON, got: {type(resp_json)} {resp_json!r}")
    item_id = resp_json.get("id")
    if isinstance(item_id, str) and item_id:
        return item_id

    status = resp_json.get("status")
    if isinstance(status, str) and status:
        m = UUID_RE.search(status)
        if m:
            return m.group(0)

    raise AssertionError(f"Cannot extract item id from response: {resp_json!r}")

def normalize_item(data: Any) -> Dict[str, Any]:
    # Нормализуем GET-ответ
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        if not data:
            raise AssertionError("Expected non-empty list with an item, got empty list")
        first = data[0]
        if isinstance(first, dict):
            return first
    raise AssertionError(f"Unexpected response type: {type(data)} body={data!r}")

@pytest.fixture(scope="session")
def base_url() -> str:
    return _base_url()

@pytest.fixture(scope="session")
def http() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    return s

@pytest.fixture(scope="session")
def seller_id() -> int:
    env = os.getenv("SELLER_ID")
    if env:
        return int(env)
    return _unique_seller_id()

@pytest.fixture()
def create_item_payload(seller_id: int) -> Dict[str, Any]:
    return {
        "sellerID": seller_id,
        "name": f"Test item QA {int(time.time())}",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }

@pytest.fixture()
def created_item_id(base_url: str, http: requests.Session, create_item_payload: Dict[str, Any]) -> str:
    # Создаём объявление и возвращаем его UUID (чтобы использовать в других тестах)
    url = f"{base_url}/api/1/item"
    r = http.post(url, json=create_item_payload, timeout=DEFAULT_TIMEOUT)
    assert r.status_code == 200, f"Create failed: {r.status_code} {r.text}"
    item_id = extract_item_id(r.json())
    uuid.UUID(item_id)  # проверка формата

    return item_id

@pytest.fixture()
def created_item(
    base_url: str,
    http: requests.Session,
    create_item_payload: Dict[str, Any],
    created_item_id: str,
) -> Dict[str, Any]:
    url = f"{base_url}/api/1/item/{created_item_id}"
    r = http.get(url, timeout=DEFAULT_TIMEOUT)
    assert r.status_code == 200, f"GET created item failed: {r.status_code} {r.text}"

    obj = normalize_item(r.json())

    # Минимальные проверки 
    assert obj.get("id") == created_item_id
    assert obj.get("sellerId") == create_item_payload["sellerID"]
    assert obj.get("name") == create_item_payload["name"]
    assert obj.get("price") == create_item_payload["price"]
    assert obj.get("createdAt")
    stats = obj.get("statistics")
    assert isinstance(stats, dict), f"Missing statistics: {obj!r}"
    assert isinstance(stats.get("likes"), int)
    assert isinstance(stats.get("viewCount"), int)
    assert isinstance(stats.get("contacts"), int)

    return obj
