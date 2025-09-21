from flask import Flask, redirect, request, make_response
import os
import threading
import time
import hashlib

app = Flask(__name__)
COUNTER_FILE = os.path.join(os.path.dirname(__file__), "counter.txt")
lock = threading.Lock()

# Временное хранилище для недавних посещений (защита от дублей в пределах N секунд)
recent_visitors = {}  # {visitor_key: timestamp}
RECENT_TIMEOUT = 5  # секунд — если тот же пользователь зашёл раньше, чем 5 сек назад — игнорируем

def get_visitor_key():
    """Генерируем уникальный ключ для посетителя на основе IP и User-Agent"""
    ip = request.remote_addr or "unknown"
    ua = request.headers.get('User-Agent', '') or "unknown"
    key_str = f"{ip}:{ua}"
    return hashlib.md5(key_str.encode()).hexdigest()

@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/run')
def track_and_redirect():
    visitor_key = get_visitor_key()
    now = time.time()

    # Очищаем устаревшие записи (опционально, чтобы не рос словарь бесконечно)
    with lock:
        # Удаляем записи старше RECENT_TIMEOUT
        to_delete = [key for key, ts in recent_visitors.items() if now - ts > RECENT_TIMEOUT]
        for key in to_delete:
            recent_visitors.pop(key, None)

        # Проверяем, не было ли посещения от этого пользователя совсем недавно
        if visitor_key in recent_visitors:
            print(f"Дубль от {visitor_key} — игнорируем")
            response = make_response(redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302))
            # На всякий случай ставим куку, если её ещё нет
            if not request.cookies.get('visited'):
                response.set_cookie('visited', 'true', max_age=3600)
            return response

        # Помечаем, что этот пользователь сейчас "в обработке"
        recent_visitors[visitor_key] = now

    # Теперь проверяем куки — если есть, то вообще не увеличиваем
    if request.cookies.get('visited') == 'true':
        print("Уже посещали (кука) — не увеличиваем счётчик")
        return redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302)

    # Увеличиваем счётчик
    count = 0
    with lock:
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r") as f:
                    count = int(f.read().strip())
            except Exception:
                count = 0

        count += 1

        try:
            with open(COUNTER_FILE, "w") as f:
                f.write(str(count))
        except Exception as e:
            print(f"Ошибка записи счётчика: {e}")

    print(f"Сканирований: {count}")

    # Отправляем редирект с кукой
    response = make_response(redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302))
    response.set_cookie('visited', 'true', max_age=3600)
    return response

@app.route('/reset')
def reset_counter():
    with lock:
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
        recent_visitors.clear()  # если используешь recent_visitors из предыдущего решения
    print("Счетчик сброшен")

    response = make_response("<h2>✅ Счётчик сброшен на 0 и кука удалена!</h2><p><a href='/run'>← Вернуться</a></p>")
    response.set_cookie('visited', '', expires=0)  # ← вот эта строка удаляет куку
    return response
