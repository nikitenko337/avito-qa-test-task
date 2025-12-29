# Структура проекта
```
├── README.md                      # структура проекта и инструкция
├── requirements.txt               # зависимости
│
├── TASK_1/                        # задание 1
│   ├── BUGS.md                    # баг-репорты по заданию 1
│   └── Image_bugs/                # скриншоты багов
│
└── TASK_2/                        # задание 2
    ├── BUGS_API.md                # баг-репорты (API)
    ├── TESTCASES.md               # тест-кейсы 
    ├── conftest.py                # фикстуры 
    ├── test_post_item.py          # автотесты: POST /item
    ├── test_get_item_by_id.py     # автотесты: GET /item/{id}
    ├── test_get_items_by_seller.py# автотесты: GET /item?sellerId=...
    └── test_get_statistic_by_id.py# автотесты: GET /statistic/{id}
```
# README.md — запуск автотестов API (pytest)

## 1) Что нужно заранее
- **Python 3.10+** (рекомендуется 3.11)
- Доступ в интернет до стенда: `https://qa-internship.avito.com`

Проверка, что Python установлен:
```bash
python --version
```
Если команда не находится — установите Python с официального сайта и при установке на Windows отметьте галочку **“Add python.exe to PATH”**.

## 2) Склонировать проект
В терминале/PowerShell:
```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd <ПАПКА_ПРОЕКТА>
```

## 3) Создать и активировать виртуальное окружение

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 4) Установить зависимости

```bash
pip install -r requirements.txt
```

## 5) Запуск тестов

Перейдите в папку с тестами:
```bash
cd <ПАПКА_С_ТЕСТАМИ>
```

Запуск:
```bash
python -m pytest -s
```

Если нужно короче (без подробного вывода):
```bash
python -m pytest -q
```

## 6) Типичные проблемы

### Ошибка: `No module named pytest`
Значит pytest не установлен в текущем окружении:
```bash
pip install pytest
```
И запускайте именно так:
```bash
python -m pytest -s
```

### Ошибка активации venv в PowerShell
Разрешите запуск скриптов (один раз):
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Готово: после этих шагов тесты запускаются одной командой `python -m pytest -s`.
