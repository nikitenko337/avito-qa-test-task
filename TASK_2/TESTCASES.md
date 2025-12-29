## Общие условия и данные

- base_url берётся из переменной окружения BASE_URL, иначе используется https://qa-internship.avito.com.
- seller_id берётся из SELLER_ID, иначе генерируется уникальный.
- Для сценариев, где нужен itemId:
  - выполняется POST /api/1/item;
  - itemId извлекается:
    - либо из поля id в JSON-ответе,
    - либо UUID ищется в строке status (например: "Сохранили объявление - <uuid>");
  - дополнительно проверяется, что itemId — валидный UUID.
- Для сценариев, где нужен created_item:
  - выполняется GET /api/1/item/{itemId};
  - ответ нормализуется (если пришёл list — берётся первый элемент);
  - проверяется структура и значения (id/sellerId/name/price/createdAt/statistics).

# 1) POST /api/1/item (test_post_item.py)

## TC-AT-POST-001 — test_create_item_success
**Цель:** успешное создание объявления.  
**Запрос:** POST /api/1/item  
**Headers:** Content-Type: application/json, Accept: application/json  
**Body (пример):**
```json
{
  "sellerID": 777777,
  "name": "Test item create success",
  "price": 1000,
  "statistics": { "likes": 1, "viewCount": 1, "contacts": 1 }
}
```

**Шаги:**
1. Отправить запрос.
2. Проверить код ответа.
3. Извлечь itemId:
   - response.id, либо
   - UUID из response.status.
4. Провалидировать, что itemId соответствует формату UUID.

**Ожидаемый результат:**
- HTTP 200 OK
- itemId успешно извлечён и является валидным UUID.

## TC-AT-POST-002 — test_create_item_validation_errors_400[missing_sellerID]
**Цель:** проверить обязательность sellerID.  
**Запрос:** POST /api/1/item 
**Headers:** Content-Type: application/json, Accept: application/json 
**Body:**
```json
{
  "name": "Test item QA missing sellerID",
  "price": 1000,
  "statistics": { "likes": 1, "viewCount": 1, "contacts": 1 }
}
```

**Шаги:**
1. Отправить запрос без sellerID.
2. Проверить код ответа.

**Ожидаемый результат:**
- HTTP 400 Bad Request

---

## TC-AT-POST-003 — test_create_item_validation_errors_400[price_wrong_type]
**Цель:** проверить валидацию типа price.  
**Запрос:** POST /api/1/item  
**Headers:** Content-Type: application/json, Accept: application/json  
**Body:**
```json
{
  "sellerID": 777777,
  "name": "Test item wrong price type",
  "price": "1000",
  "statistics": { "likes": 1, "viewCount": 1, "contacts": 1 }
}
```

**Шаги:**
1. Отправить запрос с price строкой.
2. Проверить код ответа.

**Ожидаемый результат:**
- HTTP 400 Bad Request

---

# 2) GET /api/1/item/{id} (test_get_item_by_id.py)

## TC-AT-GETITEM-001 — test_get_item_by_id_success
**Предусловие:** создано объявление, получен created_item_id.  
**Цель:** получить объявление по существующему id.  
**Запрос:** GET /api/1/item/{created_item_id}  
**Headers:** Accept: application/json

**Шаги:**
1. Отправить запрос.
2. Проверить код ответа 200.
3. Проверить формат JSON:
   - либо list (и он не пустой),
   - либо dict.
4. Получить объект объявления:
   - obj = data[0], если data — list,
   - иначе obj = data.
5. Проверить:
   - obj["id"] == created_item_id
   - присутствуют поля sellerId, name, price, statistics, createdAt.

**Ожидаемый результат:**
- HTTP 200 OK
- корректный объект объявления в ответе.

## TC-AT-GETITEM-002 — test_get_item_by_id_invalid_id_400[not_uuid_1]
**Цель:** проверить валидацию формата id (не UUID).  
**Запрос:** GET /api/1/item/no-such-id-123456  
**Headers:** Accept: application/json

**Шаги:**
1. Отправить запрос.
2. Проверить код ответа.

**Ожидаемый результат:**
- HTTP 400 Bad Request

## TC-AT-GETITEM-003 — test_get_item_by_id_invalid_id_400[not_uuid_2]
**Цель:** проверить валидацию формата id (ещё один невалидный вариант).  
**Запрос:** GET /api/1/item/not-a-uuid 
**Headers:** Accept: application/json

**Шаги:**
1. Отправить запрос.
2. Проверить код ответа.

**Ожидаемый результат:**
- HTTP 400 Bad Request

---

## TC-AT-GETITEM-004 — test_get_item_by_id_not_found_valid_uuid
**Цель:** поведение при валидном UUID, которого нет.  
**Запрос:** GET /api/1/item/{missing_uuid} (UUID генерируется случайно)  
**Headers:** Accept: application/json

**Шаги:**
1. Сгенерировать missing_uuid (валидный UUID).
2. Отправить запрос.
3. Проверить код ответа: допускается 404 или 200.
4. Если 200, проверить что тело пустое ([] или {}).

**Ожидаемый результат:**
- HTTP 404 Not Found **или** HTTP 200 OK и пустой JSON ([] / {}).

# 3) GET /api/1/{sellerID}/item (test_get_items_by_seller.py)

## TC-AT-SELLERITEMS-001 — test_get_items_by_seller_success
**Предусловие:** создано объявление и получен created_item (через GET по id).  
**Цель:** получить список объявлений продавца и убедиться, что созданное объявление присутствует.  
**Запрос:** GET /api/1/{seller_id}/item 
**Headers:** Accept: application/json

**Шаги:**
1. Взять seller_id = created_item["sellerId"], item_id = created_item["id"].
2. Отправить GET /api/1/{seller_id}/item.
3. Проверить код ответа 200.
4. Проверить, что ответ — list.
5. Проверить, что в списке есть элемент с id == item_id.

**Ожидаемый результат:**
- HTTP 200 OK
- список содержит созданное объявление.

## TC-AT-SELLERITEMS-002 — test_get_items_by_seller_bad_sellerid_400[letters]
**Цель:** валидация sellerID (не число).  
**Запрос:** GET /api/1/abc/item  
**Headers:** Accept: application/json

**Шаги:**
1. Отправить запрос.
2. Проверить код ответа.

**Ожидаемый результат:**
- HTTP 400 Bad Request

## TC-AT-SELLERITEMS-003 — test_get_items_by_seller_bad_sellerid_400[mixed]
**Цель:** валидация sellerID (смешанный формат).  
**Запрос:** GET /api/1/12ab/item  
**Headers:** Accept: application/json

**Шаги:**
1. Отправить запрос.
2. Проверить код ответа.

**Ожидаемый результат:**
- HTTP 400 Bad Request

# 4) GET /api/1/statistic/{id} (test_get_statistic_by_id.py)

## TC-AT-STAT-001 — test_get_statistic_by_id_success
**Предусловие:** создано объявление, получен created_item_id.  
**Цель:** получить статистику по существующему itemId.  
**Запрос:** GET /api/1/statistic/{created_item_id}`  
**Headers:** Accept: application/json

**Шаги:**
1. Отправить запрос.
2. Проверить код ответа 200.
3. Проверить, что ответ — list и он не пустой.
4. Взять stat = data[0] и проверить:
   - stat["likes"] — int
   - `stat["viewCount"] — int
   - stat["contacts"] — int

**Ожидаемый результат:**
- HTTP 200 OK
- корректная структура и типы полей статистики.

## TC-AT-STAT-002 — test_get_statistic_invalid_id_400[not_uuid_1]
**Цель:** проверить валидацию формата `id` в статистике (не UUID).  
**Запрос:** GET /api/1/statistic/no-such-id-123456  
**Headers:** Accept: application/json

**Шаги:**
1. Отправить запрос.
2. Проверить код ответа.

**Ожидаемый результат:**
- HTTP 400 Bad Request

## TC-AT-STAT-003 — test_get_statistic_invalid_id_400[not_uuid_2]
**Цель:** проверить валидацию формата id в статистике (ещё один невалидный вариант).  
**Запрос:** GET /api/1/statistic/not-a-uuid  
**Headers:** Accept: application/json

**Шаги:**
1. Отправить запрос.
2. Проверить код ответа.

**Ожидаемый результат:**
- HTTP 400 Bad Request

## TC-AT-STAT-004 — test_get_statistic_not_found_valid_uuid
**Цель:** поведение статистики при валидном UUID, которого нет.  
**Запрос:** GET /api/1/statistic/{missing_uuid} (UUID генерируется случайно)  
**Headers:** Accept: application/json

**Шаги:**
1. Сгенерировать missing_uuid (валидный UUID).
2. Отправить запрос.
3. Проверить код ответа: допускается 404 или 200.
4. Если 200, проверить что тело пустое ([] или {}).

**Ожидаемый результат:**
- HTTP 404 Not Found или HTTP 200 OK и пустой JSON ([] / {}).

