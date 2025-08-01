st = """
👋 Привіт! Я — бот NumberMind.
Готовий зіграти з тобою в гру! 🧠🔢
"""

hp = """
🎯 Мета гри — відгадати секретне число, яке заздалегідь загадано ботом.
🔢 Як це працює:
Ви вибираєте кількість цифр у коді (від 2 до 10).
Бот загадує секретне число у якому всі цифри різні.
Ви намагаєтесь відгадати це число, надсилаючи свої версії.
Бот надає вам відповідь до кожної спроби:
перше число — кількість цифр, які вгадані.
друге число — скільки з них стоять на своєму місці.

📌 Приклад:

Секретне число:  4271
Ваше припущення: 1234

Результат - 3 : 1 
— 3 цифри вгадані (це 1, 2 та 4); 
— 1 з них стоїть на своєму місці (це 2).
"""

exit = """
Гру несподівано завершено. Можеш змінити складність гри та зіграти ще раз, вибравши пункт меню.
"""

challenge_NO = """
🎯 NumberMind Challenge!

Привіт, друже! 👋
Готовий прокачати свою логіку та інтуїцію? 🔍🧠

Тут ти зможеш:
✅ Відгадувати секретні коди
✅ Змагатися з іншими гравцями
✅ Потрапити до списку переможців!

🔔 Слідкуй за оновленнями — зовсім скоро стартують нові завдання!

Готуйся до розумової битви! 💥

"""

def challenge_YES(ch):
    data = ch.split('-')
    res = ''
    for i in range(2, 11):
        res += f"🔢 {i}-цифрових кодів: {data[i-2]} шт.\n"

    return (
        "🎯 NumberMind Challenge!\n\n"
        "Привіт, друже!\n"
        "Готовий випробувати свою логіку та інтуїцію? 🔍\n\n"
        "🧠 Твоя мета Відгадати:\n"
        f"{res}\n"
        "🏆 Якщо впораєшся — потрапиш у таблицю переможців!\n"
        "Запиши своє ім’я в історію NumberMind 💥\n\n"
        "💡 Успіху, розумнику!\n"
    )

