from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from models import Task
from game import add_xp, TASKS, can_click, generate_plan
from db import get_user, reset_daily, update_user
from shop import SHOP

app = FastAPI()


# =========================
# 🔥 SAFE USER INIT
# =========================
def ensure_user(uid):
    user = get_user(uid)
    if not user:
        return None
    return user


# =========================
# 🧠 PLAN GENERATOR (FIXED)
# =========================
@app.post("/generate-plan")
def plan(data: dict):
    user = get_user(data["user_id"])
    if not user:
        return {"error": "user not found"}

    safe_data = {
        "goal": user[7] or "discipline",
        "weight": user[5] or 70,
        "height": user[4] or 175,
        "age": user[3] or 20,
        "day": 1,
        "bad_habit": "smoking"
    }

    return generate_plan(safe_data)


# =========================
# ⚔️ COMPLETE TASK (CORE LOOP)
# =========================
@app.post("/complete-task")
def complete_task(data: Task):

    user = ensure_user(data.user_id)
    if not user:
        return {"error": "user not found"}

    if not can_click(data.user_id):
        return {"error": "слишком быстро"}

    # =========================
    # 📅 DAILY RESET (FIX ORDER)
    # =========================
    reset_daily(data.user_id)

    # =========================
    # TASK CHECK
    # =========================
    if data.task not in TASKS:
        return {"error": "неизвестная задача"}

    xp, stat = TASKS[data.task]

    # =========================
    # XP ADD
    # =========================
    result = add_xp(data.user_id, xp, stat)

    user = get_user(data.user_id)

    # =========================
    # 🔥 STREAK FIX (V6 ADDITION)
    # =========================
    streak = user[9] or 0
    update_user(data.user_id, "streak", streak + 1)

    # =========================
    # RESPONSE
    # =========================
    return {
        **result,
        "streak": streak + 1
    }


# =========================
# 🛒 SHOP API (FIXED)
# =========================
@app.get("/shop")
def shop():
    return {"shop": SHOP}


# =========================
# 🌐 MAIN UI
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>⚔️ ВОИН V6</title>

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
}

.bar{
width:340px;
height:10px;
background:#333;
border-radius:5px;
}

.fill{
height:10px;
background:lime;
width:0%;
}

.shop{
background:#222;
padding:8px;
margin:5px;
border-radius:8px;
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
async function act(task){

let uid = 1;

try{
 uid = window.Telegram.WebApp.initDataUnsafe.user.id;
}catch(e){}

const r = await fetch("/complete-task",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({user_id:uid,task:task})
});

const d = await r.json();

if(d.error){
alert(d.error);
return;
}

let need = 120 + (d.level-1)*80;
let percent = (d.xp/need)*100;

document.getElementById("level").innerText="Уровень: "+d.level;
document.getElementById("xp").innerText="Опыт: "+d.xp+" / "+need;
document.getElementById("bar").style.width=percent+"%";

document.getElementById("energy").innerText="⚡ Энергия: "+d.energy;
document.getElementById("coins").innerText="💰 Монеты: "+d.coins;
document.getElementById("streak").innerText="🔥 Серия: "+d.streak;

if(d.leveled_up){
alert("⚔️ НОВЫЙ УРОВЕНЬ!");
}
}
</script>

</body>
</html>
"""
