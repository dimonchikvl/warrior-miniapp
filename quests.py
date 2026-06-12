from datetime import date
import random

# ===== базовые квесты =====
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

# ===== ежедневные квесты =====
def generate_daily_quests():
    return random.sample(QUEST_POOL, 3)

DAILY_QUESTS = {
    "date": str(date.today()),
    "quests": generate_daily_quests()
}
