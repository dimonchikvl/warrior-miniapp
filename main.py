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
            width: 300px;
            border-radius: 12px;
        }

        button {
            width: 300px;
            padding: 12px;
            margin: 6px;
            border-radius: 10px;
            border: none;
            background: #2d6cdf;
            color: white;
            font-size: 16px;
        }

        button:active {
            transform: scale(0.98);
        }

        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 10px;
        }
    </style>
</head>
<body>

<h1>⚔️ WARRIOR</h1>

<div class="card">
    <p>Уровень: 1</p>
    <p>XP: 0 / 100</p>
</div>

<div class="stats">
    <div>💪 0</div>
    <div>🧠 0</div>
    <div>💰 0</div>
    <div>📱 0</div>
</div>

<h3>Сегодня</h3>

<button>🏋️ Тренировка</button>
<button>🚶 10000 шагов</button>
<button>🚭 Без сигарет</button>
<button>🎥 Выложить ролик</button>
<button>📚 Прочитать 10 страниц</button>

</body>
</html>
"""
