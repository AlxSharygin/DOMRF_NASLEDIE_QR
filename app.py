@app.route('/settings', methods=['GET', 'POST'])
def settings_counter():
    if request.method == 'POST':
        try:
            with open(COUNTER_FILE, "w") as f:
                f.write("0")
        except OSError:
            pass
        # Перенаправляем обратно на /settings — БЕЗ ссылки на /
        return redirect("/settings", code=302)  # ← вот это ключевое изменение

    try:
        with open(COUNTER_FILE, "r") as f:
            count = int(f.read().strip())
    except (ValueError, OSError):
        count = 0

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Сброс счётчика</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h2>🔁 Страница сброса счётчика</h2>
        <p><strong>Текущее количество переходов по QR-коду: {count}</strong></p>
        <form method="POST">
            <button type="submit">🔄 Сбросить счётчик</button>
        </form>
        <p>✅ После сброса страница обновится автоматически.</p>
    </body>
    </html>
    """
    return render_template_string(html)
