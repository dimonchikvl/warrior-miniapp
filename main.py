from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()

# =========================
# SIMPLE IN-MEMORY DB
# =========================
users = {}

def xp_needed(level):
    return 100 + (level - 1) * 50


def get_user(uid: int):
    if uid not in users:
        users[uid] = {
            "xp": 0,
            "level": 1,
            "strength": 0,
            "discipline": 0,
            "finance": 0,
            "content": 0
        }
    return users[uid]


def add_xp(uid: int, amount: int, stat: str = None):
    user = get_user(uid)

    user["xp"] += amount

    if stat:
        user[stat] += 1

    # LEVEL UP LOGIC
    needed = xp_needed(user["level"])
    if user["xp"] >= needed:
        user["xp"] -= needed
        user["level"] += 1


# =========================
# REQUEST MODEL
# =========================
class Task(BaseModel):
    user_id: int
    task: str


# =========================
# API: COMPLETE TASK
# =========================
@app.post("/complete-task")
def complete_task(data: Task):

    rewards = {
        "train": (25, "strength"),
        "steps": (20, "discipline"),
        "no_smoke": (30, "discipline"),
        "video": (25, "content"),
        "book": (15, "discipline")
    }

    if data.task not in rewards:
        return JSONResponse({"error": "unknown task"})

    xp, stat = rewards[data.task]

    add_xp(data.user_id, xp, stat)

    user = get_user(data.user_id)

    return {
        "xp": user["xp"],
        "level": user["level"],
        "strength": user["strength"],
        "discipline": user["discipline"],
        "finance": user["finance"],
        "content": user["content"]
    }


# =========================
# MINI APP FRONTEND
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Warrior RPG</title>

    <style>
        body {
            background: #0f0f0f;
            color: white;
            font-family: Arial;
            text-align: center;
            padding: 20px;
        }

        .card {
            background: #1c1c1c;
            padding: 15px;
            margin: 10px auto;
            width: 320px;
            border-radius: 12px;
        }

        button {
            width: 320px;
            padding: 12px;
            margin: 6px;
            border-radius: 10px;
            border: none;
            background: #2d6cdf;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        button:active {
            transform: scale(0.97);
        }

        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 10px;
        }
    </style>
</head>
<body>

<h1>⚔️ WARRIOR RPG</h1>

<div class="card">
    <p id="level">Уровень: 1</p>
    <p id="xp">XP: 0 / 100</p>
</div>

<div class="stats">
    <div>💪 <span id="strength">0</span></div>
    <div>🧠 <span id="discipline">0</span></div>
    <div>💰 <span id="finance">0</span></div>
    <div>📱 <span id="content">0</span></div>
</div>

<h3>Сегодня</h3>

<button onclick="complete('train')">🏋️ Тренировка</button>
<button onclick="complete('steps')">🚶 10000 шагов</button>
<button onclick="complete('no_smoke')">🚭 Без сигарет</button>
<button onclick="complete('video')">🎥 Выложить ролик</button>
<button onclick="complete('book')">📚 Прочитать 10 страниц</button>

<script>
async function complete(task) {

    // Telegram user id (если открыто в WebApp)
    let user_id = 1;

    try {
        user_id = window.Telegram.WebApp.initDataUnsafe.user.id;
    } catch (e) {}

    const res = await fetch("/complete-task", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: user_id,
            task: task
        })
    });

    const data = await res.json();

    document.getElementById("level").innerText =
        "Уровень: " + data.level;

    document.getElementById("xp").innerText =
        "XP: " + data.xp;

    document.getElementById("strength").innerText =
        data.strength;

    document.getElementById("discipline").innerText =
        data.discipline;

    document.getElementById("finance").innerText =
        data.finance;

    document.getElementById("content").innerText =
        data.content;
}
</script>

</body>
</html>
"""
