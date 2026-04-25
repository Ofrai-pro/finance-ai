# data_manager.py - работа с данными
import json
import os
from datetime import date

DATA_FILE = "data/records.json"

def load_records():
    """Загружает список всех записей из JSON-файла."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_records(records):
    """Сохраняет записи в JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def add_income(amount, source, description=""):
    """Добавляет запись о доходе."""
    record = {
        "type": "income",
        "amount": amount,
        "source": source,
        "description": description,
        "date": str(date.today())
    }
    records = load_records()
    records.append(record)
    save_records(records)
    return record
