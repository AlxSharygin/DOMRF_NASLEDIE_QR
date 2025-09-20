from flask import Flask, redirect, request
import os
from datetime import datetime

app = Flask(__name__)

COUNTER_FILE = "counter.txt"

# Создаём файл, если его нет
if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

# Обработчик favicon.ico — чтобы не увеличивал счётчик
@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content — ничего не возвращаем

@app.route('/')
def track_and_redirect():
    # Логируем информацию о запросе
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Неизвестно')
    method = request.method
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Запрос от {ip} | Метод: {method} | UA: {user_agent}")

    # Игнорируем не-GET запросы (например, HEAD от сканеров)
    if method != "GET":
        print("  → Игнорируем не-GET запрос.")
        return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302)

    count = 0

    # Безопасное чтение счётчика
    try:
        with open(COUNTER_FILE, "r") as f:
            content = f.read().strip()
            if content.isdigit():
                count = int(content)
            else:
                print(f"⚠️ Некорректное содержимое файла: '{content}'.
