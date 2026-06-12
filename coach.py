def coach_message(plan):
    if plan["type"] == "cut":
        return "🔥 Сегодня работаем на сжигание жира. Не пропускай шаги!"

    if plan["type"] == "bulk":
        return "💪 Масса растёт через дисциплину. Ешь белок!"

    return "🧠 Держи фокус. Один день = один шаг вперёд."
