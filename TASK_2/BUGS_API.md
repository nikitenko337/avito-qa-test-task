
## BUG-01 — POST /api/1/item: счётчики statistics не принимают значение 0
**Priority:** High    

**Предусловия:** API доступен.

**Шаги:**
1. Отправить запрос POST `{{baseUrl}}/api/1/item`
2. Заголовки: Accept: application/json, Content-Type: application/json
3. Тело (JSON):
```json
{
  "sellerID": 103,
  "name": "Zero stats item",
  "price": 100,
  "statistics": { "likes": 0, "viewCount": 0, "contacts": 0 }
}
```

**Фактический результат:**
- HTTP 400
- Сообщения вида: "поле likes обязательно", "поле viewCount обязательно", "поле contacts обязательно" (в зависимости от поля, которое = 0).

**Ожидаемый результат (по смыслу доки и типам):**
- 0 — валидный integer для счётчиков, запрос должен проходить с HTTP 200.

**Почему это баг:** нельзя создавать объявление с нулевой статистикой (стартовые значения обычно 0).

## BUG-02 — POST /api/1/item: успешный ответ 200 не соответствует документации
**Priority:** High  

**Предусловия:** API доступен.

**Шаги:**
1. Отправить POST `{{baseUrl}}/api/1/item`
2. Заголовки: Accept, Content-Type: application/json
3. Валидное тело:
```json
{
  "sellerID": 1023421,
  "name": "Chocolate",
  "price": 7000,
  "statistics": { "likes": 1, "viewCount": 1, "contacts": 1 }
}
```

**Фактический результат:**
- HTTP 200
- Тело ответа:
```json
{ "status": "Сохранили объявление - 786a68ba-3758-4730-8d65-a7030d13ac58" }
```

**Ожидаемый результат по документации (Success response):**
- HTTP 200
- Тело ответа — object объявления:
```json
{
  "id": "<string>",
  "sellerId": "<integer>",
  "name": "<string>",
  "price": "<integer>",
  "statistics": { "likes": "<integer>", "viewCount": "<integer>", "contacts": "<integer>" },
  "createdAt": "<string>"
}
```

**Почему это баг:** несоответствие контракта (автотесты, ориентированные на доку, ломаются).

## BUG-03 — POST /api/1/item: при ошибках типа возвращается некорректная/вводящая в заблуждение ошибка “не передано тело объявления”
**Priority:** High  

**Предусловия:** API доступен.

**Шаги (пример 1):**
1. POST `{{baseUrl}}/api/1/item`
2. Заголовки: Accept, Content-Type: application/json
3. Тело (неверный тип поля price — строка вместо integer):
```json
{
  "sellerID": 110,
  "name": "String price",
  "price": "100",
  "statistics": { "likes": 1, "viewCount": 1, "contacts": 1 }
}
```

**Шаги (пример 2):**
- Неверный тип вложенного поля:
```json
{
  "sellerID": 111,
  "name": "Bad likes type",
  "price": 100,
  "statistics": { "likes": "1", "viewCount": 1, "contacts": 1 }
}
```

**Фактический результат:**
- HTTP 400
- Тело ответа:
```json
{
  "result": { "message": "", "messages": {} },
  "status": "не передано тело объявления"
}
```

**Ожидаемый результат по документации (Bad request):**
- HTTP 400
- Тело ответа соответствует схеме:
```json
{
  "result": {
    "messages": { "<string>": "<string>" },
    "message": "<string>"
  },
  "status": "<string>"
}
```
- И сообщение должно явно указывать на причину (например: `price должен быть integer`, `statistics.likes должен быть integer`).

**Почему это баг:**
- Сообщение “не передано тело объявления” неверное (body передан).
- result.message пустой — не помогает диагностике.
- Поле status используется как текст, а не как статус/код/строка статуса по контракту.

## BUG-04 — GET /api/1/item/:id: ответ 404 не соответствует документации по формату
**Priority:** Medium  
**Предусловия:** API доступен.

**Шаги:**
1. Отправить GET `{{baseUrl}}/api/1/item/b3a1b6d2-4f3b-4b7a-9bb2-2e1a3c9f6c12` (валидный UUID, которого нет)
2. Заголовок: Accept: application/json

**Фактический результат:**
- HTTP 404
- Тело ответа:
```json
{
  "result": {
    "message": "item b3a1b6d2-4f3b-4b7a-9bb2-2e1a3c9f6c12 not found",
    "messages": null
  },
  "status": "404"
}
```

**Ожидаемый результат по документации (Not Found):**
- HTTP 404
- Тело ответа:
```json
{ "result": "<string>", "status": "<string>" }
```

**Почему это баг:** несоответствие контракта 404 (тип поля result другой: ожидается string, фактически object).


## BUG-05 — GET /api/1/statistic/:id: ответ 404 не соответствует документации по формату
**Priority:** Medium   

**Предусловия:** API доступен.

**Шаги:**
1. Отправить GET `{{baseUrl}}/api/1/statistic/b3a1b6d2-4f3b-4b7a-9bb2-2e1a3c9f6c12`
2. Заголовок: Accept: application/json

**Фактический результат:**
- HTTP 404
- Тело ответа:
```json
{
  "result": {
    "message": "statistic b3a1b6d2-4f3b-4b7a-9bb2-2e1a3c9f6c12 not found",
    "messages": null
  },
  "status": "404"
}
```

**Ожидаемый результат по документации (Not Found):**
- HTTP 404
- Тело ответа:
```json
{ "result": "<string>", "status": "<string>" }
```

**Почему это баг:** несоответствие контракта 404 для statistic.

## BUG-06 — GET /api/1/:sellerID/item: отрицательный sellerID принимается и возвращает данные
**Priority:** High  
 

**Предусловия:** API доступен.

**Шаги:**
1. Отправить GET `{{baseUrl}}/api/1/-1/item`
2. Заголовок: Accept: application/json

**Фактический результат:**
- HTTP 200
- В ответе есть объявления с sellerId: -1 (пример):
```json
[
  {
    "id": "ee04571c-4b62-4bbc-ba20-9a3e7583a94c",
    "sellerId": -1,
    "name": "Watch",
    "price": 50000,
    "statistics": { "likes": 1, "viewCount": 1, "contacts": 1 }
  }
]
```

**Ожидаемый результат:**
- HTTP 400 Bad Request
- Ошибка о некорректном идентификаторе продавца:
```json
{
  "result": { "message": "передан некорректный идентификатор продавца", "messages": {} },
  "status": "400"
}
```

**Почему это баг:** отрицательные идентификаторы обычно невалидны; это приводит к неконсистентности данных и обходу валидации.


## BUG-07 — GET /api/1/:sellerID/item: sellerID=0 возвращает 200 и пустой массив (неконсистентно с валидацией)
**Priority:** Medium    

**Предусловия:** API доступен.

**Шаги:**
1. Отправить GET `{{baseUrl}}/api/1/0/item`
2. Заголовок: Accept: application/json

**Фактический результат:**
- HTTP 200
- Тело: []

**Ожидаемый результат (если 0 невалиден):**
- HTTP 400 Bad Request с ошибкой “некорректный идентификатор продавца”

**Либо (если 0 валиден):**
- Нужно явно отразить в документации, что sellerID=0 допустим и возвращает пустой список.

**Почему это баг:** неконсистентность поведения/валидации sellerID (для одних значений 400, для 0 — 200).

