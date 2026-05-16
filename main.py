# main.py - Личный финансовый ассистент (с нейросетью)
from src.data_manager import add_income, add_expense, add_event, load_records
from src.ai_assistant import run_assistant, ai_insights

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
        print("4. ИИ-помощник (аналитика и правила)")
	print("5. Нейросеть (Gemini через OpenRouter) – получить совет")
        print("6. Выход")
        choice = input("Выберите действие (1-6): ").strip()

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
            run_assistant(records)

        elif choice == "5":
            records = load_records()
            ai_insights(records)

        elif choice == "6":
            print("До свидания!")
            break

        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()
