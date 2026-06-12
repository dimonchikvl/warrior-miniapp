from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any

from models import Task
from game import add_xp, TASKS, can_click, generate_plan, xp_needed
from db import get_user, reset_daily, update_user
from coach import coach_message
from shop import SHOP

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================================================
# 🧠 HELPER: SAFE USER
# =========================================================
def ensure_user(uid: int) -> Dict[str, Any]:
    """
    Получить пользователя или создать нового
    """
    user = get_user(uid)
    return user


# =========================================================
# 🧠 1. AI PLAN GENERATION
# =========================================================
@app.post("/generate-plan")
def plan(data: dict) -> Dict[str, Any]:
    """
    Генерация персонального плана для пользователя
    """
    user = ensure_user(data["user_id"])

    if not user:
        return {"error": "user not found"}

    safe_data = {
        "goal": user["goal"],
        "age": user["age"],
        "height": user["height"],
        "weight": user["weight"],
        "activity": user["activity"],
        "bad_habit": user["bad_habit"] or "none",
        "day": 1
    }

    return generate_plan(safe_data)


# =========================================================
# ⚔️ 2. CORE GAME LOOP
# =========================================================
@app.post("/complete-task")
def complete_task(data: Task) -> Dict[str, Any]:
    """
    Основной цикл игры: выполнение задачи
    """

    # -------------------------
    # 👤 USER CHECK
    # -------------------------
    user = ensure_user(data.user_id)
    if not user:
        return {"error": "user not found"}

    # -------------------------
    # ⛔ ANTI-SPAM
    # -------------------------
    if not can_click(data.user_id):
        return {"error": "слишком быстро"}

    # -------------------------
    # 📅 DAILY RESET (ПРАВИЛЬНОЕ МЕСТО)
    # -------------------------
    reset = reset_daily(data.user_id)
    
    # -------------------------
    # ❓ TASK VALIDATION
    # -------------------------
    if data.task not in TASKS:
        return {"error": "неизвестная задача"}

    xp, stat = TASKS[data.task]

    # -------------------------
    # 💪 XP ENGINE
    # -------------------------
    result = add_xp(data.user_id, xp, stat)

    if "error" in result:
        return result

    # -------------------------
    # 🔥 STREAK SYSTEM (FIXED LOGIC)
    # -------------------------
    user = get_user(data.user_id)
    
    # streak уже считается в reset_daily и add_xp
    streak = user["streak"]

    # -------------------------
    # 📦 RESPONSE
    # -------------------------
    return {
        **result,
        "streak": streak,
        "daily_reset": reset["reset"]
    }


# =========================================================
# 🧠 3. COACH MESSAGE
# =========================================================
@app.post("/coach")
def get_coach_message(data: dict) -> Dict[str, str]:
    """
    Получить мотивирующее сообщение от тренера
    """
    user = ensure_user(data["user_id"])
    
    if not user:
        return {"error": "user not found"}

    plan = generate_plan({
        "goal": user["goal"],
        "weight": user["weight"],
        "bad_habit": user["bad_habit"] or "none"
    })

    message = coach_message(plan, user)
    
    return {"message": message}


# =========================================================
# 🛒 SHOP API
# =========================================================
@app.get("/shop")
def shop() -> Dict[str, Any]:
    """
    Получить товары магазина
    """
    return {"shop": SHOP}


# =========================================================
# 👤 USER PROFILE
# =========================================================
@app.get("/user/{user_id}")
def get_user_profile(user_id: int) -> Dict[str, Any]:
    """
    Получить профиль пользователя
    """
    user = ensure_user(user_id)
    
    if not user:
        return {"error": "user not found"}
    
    return dict(user)


# =========================================================
# 🌐 UI
# =========================================================
@app.get("/", response_class=HTMLResponse)
def home():
    """
    Главная страница приложения
    """
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>⚔️ ВОИН V6</title>
<link rel="stylesheet" href="/static/style.css">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
body{
background:#0f0f0f;
color:white;
font-family:Arial;
text-align:center;
padding:20px;
}

.card{
background:#1c1c1c;
padding:15px;
margin:10px auto;
width:340px;
border-radius:12px;
box-shadow: 0 0 12px rgba(0,0,0,0.5);
}

button{
width:340px;
padding:12px;
margin:6px;
border-radius:10px;
border:none;
background:#2d6cdf;
color:white;
font-size:16px;
cursor:pointer;
transition: 0.2s;
}

button:hover{
background:#3b7cff;
}

button:active{
transform: scale(0.97);
}

.bar{
width:340px;
height:10px;
background:#333;
border-radius:5px;
overflow: hidden;
}

.fill{
height:10px;
background: linear-gradient(90deg, #00ff88, #00c3ff);
width:0%;
transition: width 0.3s ease;
}

.shop{
background:#222;
padding:8px;
margin:5px;
border-radius:8px;
border: 1px solid #333;
}

.stats{
display: flex;
justify-content: space-around;
margin-top: 10px;
font-size: 14px;
}

.coach-message{
background: #1a3a1a;
padding: 12px;
border-left: 3px solid #00ff88;
margin: 10px auto;
width: 340px;
text-align: left;
border-radius: 8px;
}

h1{
margin-bottom: 10px;
font-size: 22px;
}

h3{
margin-top: 20px;
color: #bbb;
}

.error{
color: #ff4444;
}

.success{
color: #44ff44;
}
</style>
</head>

<body>

<h1>⚔️ ВОИН RPG V6</h1>

<div class="card">
<p id="level">Уровень: 1</p>
<p id="xp">Опыт: 0</p>
<div class="bar"><div id="bar" class="fill"></div></div>
<p id="energy">⚡ Энергия: 100</p>
<p id="coins">💰 Монеты: 0</p>
<p id="streak">🔥 Серия: 0</p>
</div>

<div class="card" id="coach-section">
<p id="coach" class="coach-message">🧠 Загрузка...</p>
</div>

<div class="card">
<button onclick="act('train')">🏋️ Тренировка</button>
<button onclick="act('steps')">🚶 Шаги</button>
<button onclick="act('no_smoke')">🚭 Без сигарет</button>
<button onclick="act('video')">🎥 Видео</button>
<button onclick="act('book')">📚 Чтение</button>
</div>

<div class="card">
<h3>🛒 Магазин</h3>
<div class="shop">⚡ Энергия +20 — 100💰</div>
<div class="shop">📈 Буст XP — 150💰</div>
<div class="shop">💰 Монеты +50 — 120💰</div>
</div>

<script>
// ====== TELEGRAM INIT ======
let USER_ID = 1;

function initTelegram() {
    try {
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.ready();
            const user = window.Telegram.WebApp.initDataUnsafe?.user;
            if (user && user.id) {
                USER_ID = user.id;
                console.log("✅ Telegram User ID:", USER_ID);
            }
        }
    } catch (e) {
        console.log("⚠️ Telegram не доступен, используем тестовый ID:", USER_ID);
    }
}

// ====== UPDATE UI ======
function updateUI(data) {
    if (data.error) {
        alert("❌ " + data.error);
        return;
    }

    document.getElementById("level").innerText = "Уровень: " + data.level;
    document.getElementById("xp").innerText = "Опыт: " + data.xp + " / " + (120 + (data.level-1)*80);
    
    let percent = (data.xp / (120 + (data.level-1)*80)) * 100;
    document.getElementById("bar").style.width = percent + "%";
    
    document.getElementById("energy").innerText = "⚡ Энергия: " + data.energy;
    document.getElementById("coins").innerText = "💰 Монеты: " + data.coins;
    document.getElementById("streak").innerText = "🔥 Серия: " + data.streak;

    if (data.leveled_up) {
        alert("⚔️ НОВЫЙ УРОВЕНЬ!");
    }
    
    if (data.daily_reset) {
        console.log("📅 Новый день! Энергия восстановлена.");
    }
}

// ====== LOAD COACH MESSAGE ======
async function loadCoach() {
    try {
        const r = await fetch("/coach", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({user_id: USER_ID})
        });
        
        const d = await r.json();
        if (d.message) {
            document.getElementById("coach").innerText = d.message;
        }
    } catch (e) {
        console.log("⚠️ Ошибка загрузки тренера:", e);
    }
}

// ====== COMPLETE TASK ======
async function act(task) {
    try {
        const r = await fetch("/complete-task", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({user_id: USER_ID, task: task})
        });

        const d = await r.json();
        updateUI(d);
        
        // Обновить сообщение тренера
        await loadCoach();
    } catch (e) {
        console.log("❌ Ошибка:", e);
        alert("Ошибка сервера");
    }
}

// ====== INIT ======
window.addEventListener("DOMContentLoaded", function() {
    initTelegram();
    loadCoach();
});
</script>

</body>
</html>
"""
