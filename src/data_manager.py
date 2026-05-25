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
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

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

def add_expense(amount, category, description=""):
    """Добавляет запись о расходе."""
    record = {
        "type": "expense",
        "amount": amount,
        "category": category,
        "description": description,
        "date": str(date.today())
    }
    records = load_records()
    records.append(record)
    save_records(records)
    return record


def add_event(description, start_date, end_date="", planned_amount=0):
    """Добавляет запись о событии/плане."""
    record = {
        "type": "event",
        "description": description,
        "start_date": start_date,
        "end_date": end_date if end_date else start_date,
        "planned_amount": planned_amount,
        "date": str(date.today())
    }
    records = load_records()
    records.append(record)
    save_records(records)
    return record
