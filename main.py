# main.py - Личный финансовый ассистент (с отменой операций)
from src.data_manager import add_income, add_expense, add_event, load_records

def input_or_cancel(prompt, allow_empty=False):
    """Запрашивает ввод. Если allow_empty=True, пустая строка допустима.
    Если allow_empty=False, пустая строка означает отмену операции (возвращает None).
    """
    value = input(prompt).strip()
    if not value and not allow_empty:
        return None
    return value

def main():
    while True:
        print("\n===== Финансовый ассистент =====")
        print("1. Добавить доход")
        print("2. Добавить расход")
        print("3. Добавить событие/план")
        print("4. ИИ-помощник (просмотр, аналитика, советы)")
        print("5. Выход")
        choice = input("Выберите действие (1-5): ").strip()

        if choice == "1":
            print("\n--- Добавление дохода (Enter для отмены) ---")
            amount_str = input_or_cancel("Сумма: ")
            if amount_str is None:
                print("Операция отменена.")
                continue
            try:
                amount = float(amount_str.replace(" ", ""))
            except ValueError:
                print("Ошибка: сумма должна быть числом.")
                continue

            source = input_or_cancel("Источник (ЗП, подработка, подарок): ")
            if source is None:
                print("Операция отменена.")
                continue
            description = input("Комментарий (необязательно): ").strip()
            add_income(amount, source, description)
            print("Доход успешно добавлен!")

        elif choice == "2":
            print("\n--- Добавление расхода (Enter для отмены) ---")
            amount_str = input_or_cancel("Сумма: ")
            if amount_str is None:
                print("Операция отменена.")
                continue
            try:
                amount = float(amount_str.replace(" ", ""))
            except ValueError:
                print("Ошибка: сумма должна быть числом.")
                continue

            print("Категории: еда, транспорт, развлечения, здоровье, другое")
            category = input_or_cancel("Категория: ")
            if category is None:
                print("Операция отменена.")
                continue
            description = input("Комментарий (необязательно): ").strip()
            add_expense(amount, category, description)
            print("Расход успешно добавлен!")

        elif choice == "3":
            print("\n--- Добавление события/плана (Enter для отмены) ---")
            description = input_or_cancel("Описание (например, 'Сессия', 'Покупка'): ")
            if description is None:
                print("Операция отменена.")
                continue

            start_date = input_or_cancel("Дата начала (ГГГГ-ММ-ДД): ")
            if start_date is None:
                print("Операция отменена.")
                continue

            end_date = input("Дата окончания (ГГГГ-ММ-ДД, если один день — Enter): ").strip()
            planned_amount_str = input("Плановая сумма (если есть, иначе Enter): ").strip()
            try:
                planned_amount = float(planned_amount_str) if planned_amount_str else 0
            except ValueError:
                print("Ошибка: сумма должна быть числом. Событие не добавлено.")
                continue

            add_event(description, start_date, end_date, planned_amount)
            print("Событие успешно добавлено!")

        elif choice == "4":
            records = load_records()
            if not records:
                print("Записей пока нет.")
            else:
                print("\n--- Все записи ---")
                for i, rec in enumerate(records, 1):
                    if rec["type"] == "income":
                        print(f"{i}. Доход: {rec['amount']} от {rec['source']} ({rec['date']})")
                    elif rec["type"] == "expense":
                        print(f"{i}. Расход: {rec['amount']} на {rec['category']} ({rec['date']})")
                    elif rec["type"] == "event":
                        end_info = f" – {rec['end_date']}" if rec['end_date'] != rec['start_date'] else ""
                        amount_info = f", планируется: {rec['planned_amount']}" if rec['planned_amount'] else ""
                        print(f"{i}. Событие: {rec['description']} ({rec['start_date']}{end_info}{amount_info})")
                    else:
                        print(f"{i}. Неизвестный тип записи")

        elif choice == "5":
            print("До свидания!")
            break

        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()
