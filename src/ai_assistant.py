# ai_assistant.py – ИИ-помощник (аналитика, прогнозы, советы)
from datetime import date, datetime, timedelta
from collections import defaultdict

def show_analytics(records):
    """Выводит базовую аналитику: баланс, проценты по категориям."""
    if not records:
        print("Записей пока нет.")
        return

    total_income = sum(r["amount"] for r in records if r["type"] == "income")
    total_expense = sum(r["amount"] for r in records if r["type"] == "expense")
    balance = total_income - total_expense

    print("\n===== Финансовая аналитика =====")
    print(f"💰 Общий доход: {total_income:.2f} ₽")
    print(f"💸 Общий расход: {total_expense:.2f} ₽")
    print(f"📊 Баланс: {balance:.2f} ₽")

    if total_expense > 0:
        categories = defaultdict(float)
        for r in records:
            if r["type"] == "expense":
                categories[r["category"]] += r["amount"]
        print("\n📌 Расходы по категориям:")
        for cat, amt in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            pct = (amt / total_expense) * 100
            print(f"   {cat}: {amt:.2f} ₽ ({pct:.1f}%)")
    print()

def check_category_alert(records, category="развлечения", threshold=30):
    """Предупреждает, если доля указанной категории превышает порог."""
    total = sum(r["amount"] for r in records if r["type"] == "expense")
    cat_total = sum(r["amount"] for r in records if r["type"] == "expense" and r["category"] == category)
    if total > 0 and (cat_total / total) * 100 > threshold:
        print(f"⚠️ Внимание! Ваши траты на «{category}» составляют {cat_total:.2f} ₽ — это {(cat_total/total)*100:.1f}% от всех расходов.")
        print("   Совет: попробуйте сократить эту категорию.\n")
        return True
    return False

def predict_next_month(records):
    """Прогнозирует остаток на следующий месяц на основе среднего за последние 3 месяца."""
    today = date.today()
    monthly_income = defaultdict(float)
    monthly_expense = defaultdict(float)

    for r in records:
        try:
            d = datetime.strptime(r["date"], "%Y-%m-%d").date()
        except:
            continue
        if r["type"] == "income":
            monthly_income[(d.year, d.month)] += r["amount"]
        elif r["type"] == "expense":
            monthly_expense[(d.year, d.month)] += r["amount"]

    months = sorted(set(list(monthly_income.keys()) + list(monthly_expense.keys())), reverse=True)
    last_months = months[:3]
    if not last_months:
        print("Недостаточно данных для прогноза (нужны записи за несколько месяцев).\n")
        return

    avg_income = sum(monthly_income[m] for m in last_months) / len(last_months)
    avg_expense = sum(monthly_expense[m] for m in last_months) / len(last_months)
    predicted_balance = avg_income - avg_expense

    print(f"📈 Прогноз на следующий месяц (на основе среднего за {len(last_months)} мес.):")
    print(f"   Ожидаемый доход: ~{avg_income:.2f} ₽")
    print(f"   Ожидаемый расход: ~{avg_expense:.2f} ₽")
    print(f"   Прогнозируемый остаток: ~{predicted_balance:.2f} ₽\n")

    if predicted_balance < 0:
        print("⚠️ Прогноз отрицательный – стоит сократить расходы.\n")
    else:
        print("✅ Остаток положительный, но продолжайте следить за тратами.\n")

def analyze_events(records):
    """Анализирует события и даёт советы (сессия, плановые покупки)."""
    today = date.today()
    for r in records:
        if r["type"] != "event":
            continue
        try:
            start = datetime.strptime(r["start_date"], "%Y-%m-%d").date()
            end = datetime.strptime(r["end_date"], "%Y-%m-%d").date()
        except:
            continue

        if "сессия" in r["description"].lower() or "экзамен" in r["description"].lower():
            if start <= today <= end:
                print(f"📚 У вас сейчас: {r['description']} (с {r['start_date']} по {r['end_date']}).")
                print("   Совет: сократите развлечения, чтобы сосредоточиться на учёбе.\n")
            elif today < start:
                days_left = (start - today).days
                print(f"⏰ Скоро {r['description']} (через {days_left} дней, с {r['start_date']} по {r['end_date']}).")
                print("   Совет: начинайте сокращать необязательные траты и готовьтесь.\n")

        if r["planned_amount"] and r["planned_amount"] > 0 and start > today:
            months_left = max(1, (start.year - today.year) * 12 + (start.month - today.month))
            monthly_save = r["planned_amount"] / months_left
            print(f"🎯 Плановая покупка: {r['description']} на {r['planned_amount']:.2f} ₽ (к {r['start_date']}).")
            print(f"   Осталось ~{months_left} мес. Необходимо откладывать по {monthly_save:.2f} ₽ в месяц.\n")

def run_assistant(records):
    """Главная функция ИИ-помощника – вызывает все аналитические блоки."""
    show_analytics(records)
    check_category_alert(records)
    predict_next_month(records)
    analyze_events(records)

def ai_insights(records):
    """Отправляет финансовую сводку через OpenRouter (бесплатный Gemini) и печатает рекомендацию."""
    from openai import OpenAI
    from collections import defaultdict

    # Собираем сводку для нейросети
    total_income = sum(r["amount"] for r in records if r["type"] == "income")
    total_expense = sum(r["amount"] for r in records if r["type"] == "expense")
    balance = total_income - total_expense

    categories = defaultdict(float)
    for r in records:
        if r["type"] == "expense":
            categories[r["category"]] += r["amount"]

    summary = f"Доходы: {total_income:.2f} ₽, расходы: {total_expense:.2f} ₽, баланс: {balance:.2f} ₽.\n"
    if categories:
        summary += "Расходы по категориям:\n"
        for cat, amt in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            pct = (amt / total_expense) * 100 if total_expense > 0 else 0
            summary += f"  {cat}: {amt:.2f} ₽ ({pct:.1f}%)\n"
    else:
        summary += "Нет данных о расходах.\n"

    today = date.today()
    events = [r for r in records if r["type"] == "event"]
    if events:
        summary += "Предстоящие события:\n"
        for e in events:
            summary += f"  {e['description']} с {e['start_date']} по {e['end_date']}"
            if e.get("planned_amount") and e["planned_amount"] > 0:
                summary += f", плановая сумма {e['planned_amount']} ₽"
            summary += "\n"

    prompt = (
        "Ты — персональный финансовый ассистент. Проанализируй данные пользователя и дай совет: "
        "как лучше распределить бюджет, на что обратить внимание, как накопить на цели. "
        "Будь конкретным и доброжелательным. Не используй общих фраз, опирайся на цифры.\n\n"
        f"Данные:\n{summary}"
    )

    try:
        client = OpenAI(
            api_key="ТВОЙ_OPENROUTER_КЛЮЧ",
          base_url="https://openrouter.ai/api/v1"
        )
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": "Ты — полезный финансовый помощник."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        advice = response.choices[0].message.content
        print("\n===== Рекомендация от ИИ-ассистента (через OpenRouter) =====")
        print(advice)
    except Exception as e:
        print(f"\nОшибка при обращении к OpenRouter API: {e}")
        print("Проверьте ключ или подключение к интернету.")
