# main.py - Личный финансовый ассистент с доходом и расходом
from src.data_manager import add_income, add_expense, load_records

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
            print("\n--- Добавление дохода ---")
            amount = float(input("Сумма: "))
            source = input("Источник (ЗП, подработка, подарок): ").strip()
            description = input("Комментарий (необязательно): ").strip()
            add_income(amount, source, description)
            print("Доход успешно добавлен!")

        elif choice == "2":
            print("\n--- Добавление расхода ---")
            amount = float(input("Сумма: "))
            print("Категории: еда, транспорт, развлечения, здоровье, другое")
            category = input("Категория: ").strip().lower()
            description = input("Комментарий (необязательно): ").strip()
            add_expense(amount, category, description)
            print("Расход успешно добавлен!")

        elif choice == "3":
            print(">>> Функция 'Добавить событие/план' пока не реализована.")

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
                    else:
                        print(f"{i}. {rec['type']} (детали пока недоступны)")

        elif choice == "5":
            print("До свидания!")
            break

        else:
            print("Неверный ввод, попробуйте снова.")

if __name__ == "__main__":
    main()
