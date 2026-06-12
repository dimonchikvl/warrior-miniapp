from pydantic import BaseModel
from typing import Optional


# =========================
# ⚔️ ЗАДАЧИ (кнопки игры)
# =========================
class Task(BaseModel):
    """
    Нажатие на кнопку задачи
    """
    user_id: int
    task: str


# =========================
# 🧠 ONBOARDING (анкета пользователя)
# =========================
class UserInit(BaseModel):
    """
    Регистрация игрока (онбординг)
    """
    user_id: int

    goal: str                 # cut / bulk / discipline / content
    age: Optional[int] = 0
    height: Optional[int] = 0
    weight: Optional[int] = 0

    activity: Optional[str] = "low"
    bad_habit: Optional[str] = "none"


# =========================
# 📊 PLAN REQUEST (AI план)
# =========================
class PlanRequest(BaseModel):
    """
    Запрос на генерацию плана
    """
    user_id: int


# =========================
# 🛒 SHOP PURCHASE (на будущее)
# =========================
class ShopAction(BaseModel):
    """
    Покупки в магазине
    """
    user_id: int
    item_id: str
