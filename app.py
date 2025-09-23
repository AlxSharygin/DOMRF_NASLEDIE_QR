from flask import Flask, redirect, request, make_response
import os
import threading
import time
import hashlib

app = Flask(__name__)
COUNTER_FILE = os.path.join(os.path.dirname(__file__), "counter.txt")
lock = threading.Lock()

# Временное хранилище для защиты от дублей
recent_visitors = {}
RECENT_TIMEOUT = 5  # секунд

def get_visitor_key():
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

    with lock:
        # Очищаем устаревшие записи
        to_delete = [key for key, ts in recent_visitors.items() if now - ts > RECENT_TIMEOUT]
        for key in to_delete:
            recent_visitors.pop(key, None)

        # Защита от параллельных дублей
        if visitor_key in recent_visitors:
            print(f"Дубль от {visitor_key} — игнорируем")
            response = make_response(redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302))
            if not request.cookies.get('visited'):
                response.set_cookie('visited', 'true', max_age=3600, path='/')
            return response

    # Если кука уже есть — не увеличиваем
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

    # Редирект + установка куки на весь сайт
    response = make_response(redirect("https://xn--80aicbopm7a.xn--d1aqf.xn--p1ai/", code=302))
    response.set_cookie('visited', 'true', max_age=3600, path='/')
    return response

@app.route('/reset')
def reset_counter():
    with lock:
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
        recent_visitors.clear()
    print("✅ Счётчик сброшен")

    return """
    <h2>✅ Счётчик успешно сброшен на 0!</h2>
    <p>Чтобы заново увеличить счётчик при переходе — <a href="/clear-cookie">удалите куку</a>.</p>
    <p><a href="/run">← Вернуться к ссылке</a></p>
    """
@app.route('/statistics')
def statistics():
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Переход зафиксирован</title><meta charset="utf-8"></head>
    <body style="text-align:center; padding:50px; font-family:Arial;">
        <h2>✅ Количество переходов на портал Наследие.дом.рф через QR-код Развития регионального бизнеса</h2>
        <p><strong>Всего переходов: {count}</strong></p>
        <p><a href="/">← Вернуться на главную</a></p>
    </body>
    </html>
    """

@app.route('/clear-cookie')
def clear_cookie():
    print("🍪 Удаляем куку 'visited'...")
    response = make_response("""
    <h2>🍪 Кука 'visited' удалена!</h2>
    <p>Теперь при переходе по <a href="/run">/run</a> счётчик снова увеличится.</p>
    <p><a href="/run">← Перейти по ссылке</a></p>
    """)
    # Удаляем куку для всего сайта
    response.set_cookie('visited', '', expires=0, path='/')
    recent_visitors.clear()
    print("✅recent_visitors очищены")
    return response

