# qt-labs

Репозиторий практических работ.

## Структура

- `pr1/` — Практична робота №1. Інтеграція зовнішнього REST API (FastAPI + Open-Meteo)

## Запуск pr1

cd pr1
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

Открыть: http://127.0.0.1:8000