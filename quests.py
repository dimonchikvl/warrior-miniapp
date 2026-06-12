from datetime import date
import random

# =========================
# 📦 БАЗОВЫЕ КВЕСТЫ
# =========================
# Это список всех возможных заданий в игре
QUEST_POOL = [
    {
        "id": "train",
        "title": "🏋️ Тренировка",
        "xp": 40,
        "stat": "strength"
    },
    {
        "id": "steps",
        "title": "🚶 10000 шагов",
        "xp": 30,
        "stat": "discipline"
    },
    {
        "id": "no_smoke",
        "title": "🚭 Без сигарет",
        "xp": 50,
        "stat": "discipline"
    },
    {
        "id": "video",
        "title": "🎥 Выложить видео",
        "xp": 40,
        "stat": "content"
    },
    {
        "id": "book",
        "title": "📚 Прочитать 10 страниц",
        "xp": 20,
        "stat": "discipline"
    }
]


# =========================
# 🎯 ГЕНЕРАЦИЯ ЕЖЕДНЕВНЫХ КВЕСТОВ
# =========================
def generate_daily_quests():
    """
    Выбирает случайные квесты на день
    """
    return random.sample(QUEST_POOL, 3)


# =========================
# 📅 DAILY QUEST STATE (FIX V6)
# =========================
# ВАЖНО: это теперь "черновик состояния"
# его нужно ОБНОВЛЯТЬ каждый день в main.py / game.py
DAILY_QUESTS = {
    "date": str(date.today()),
    "quests": generate_daily_quests()
}


# =========================
# 🔥 ОБНОВЛЕНИЕ КВЕСТОВ ПО ДНЮ
# =========================
def refresh_daily_quests():
    """
    Если день поменялся — создаём новые квесты
    """
    today = str(date.today())

    if DAILY_QUESTS["date"] != today:
        DAILY_QUESTS["date"] = today
        DAILY_QUESTS["quests"] = generate_daily_quests()

    return DAILY_QUESTS


# =========================
# 🎮 ПОЛУЧИТЬ КВЕСТ ПО ID
# =========================
def get_quest_by_id(qid: str):
    """
    Возвращает квест по его ID
    """
    for q in QUEST_POOL:
        if q["id"] == qid:
            return q
    return None
