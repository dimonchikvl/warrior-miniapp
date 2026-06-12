from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Warrior</title>
</head>
<body>

<h1>⚔️ WARRIOR</h1>

<p>Уровень: 1</p>
<p>XP: 0 / 100</p>

<p>💪 Сила: 0</p>
<p>🧠 Дисциплина: 0</p>
<p>💰 Финансы: 0</p>
<p>📱 Контент: 0</p>

<hr>

<h3>Сегодня</h3>

<button>Тренировка</button><br><br>
<button>10000 шагов</button><br><br>
<button>Без сигарет</button><br><br>
<button>Выложить ролик</button><br><br>
<button>Прочитать 10 страниц</button>

</body>
</html>
"""
