from flask import Flask, redirect, request, render_template_string
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

# Инициализация файла счётчика
def init_counter():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
    else:
        try:
            with open(COUNTER_FILE, "r") as f:
                content = f.read().strip()
                int(content)
        except (ValueError, OSError):
            with open(COUNTER_FILE, "w") as f:
                f.write("0")

init_counter()


# 🚀 Главная страница — увеличивает счётчик и сразу редиректит
@app.route('/')
def track_and_redirect():
    try:
        with open(COUNTER_FILE, "r") as f:
            count = int(f.read().strip())
    except (ValueError, OSError):
        count = 0

    count += 1

    try:
        with open(COUNTER_FILE, "w") as f:
            f.write(str(count))
    except OSError:
        pass

    print(f"Сканирований: {count}")
    return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302)


# ⚙️ Страница настроек — НИКОГДА не
