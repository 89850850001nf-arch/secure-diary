from flask import Flask, request, redirect, url_for, render_template_string, session, abort
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import html
import secrets

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_diary' # Секретный ключ для сессий
DB_NAME = 'diary.db'

# --- ЗАЩИТА CSRF ---
def get_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

def check_csrf():
    if session.get('csrf_token') != request.form.get('csrf_token'):
        abort(403, description="ОШИБКА CSRF: Запрос отклонен.")

# --- ИНИЦИАЛИЗАЦИЯ БД ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Таблица пользователей
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT)''')
    # Таблица записей (привязаны к пользователю)
    c.execute('''CREATE TABLE IF NOT EXISTS notes 
                 (id INTEGER PRIMARY KEY, user_id INTEGER, content TEXT, date TEXT)''')
    conn.commit()
    conn.close()

# --- ГЛАВНАЯ СТРАНИЦА (ВХОД ИЛИ ДНЕВНИК) ---
@app.route('/')
def index():
    if 'user_id' not in session:
        # Если не вошел - показываем страницу входа
        token = get_csrf_token()
        return f"""
        <html><body style="font-family: Arial; padding: 40px; text-align: center;">
            <h1>🔒 Секретный Дневник</h1>
            <p>Войдите или <a href="/register">зарегистрируйтесь</a></p>
            <form method="POST" action="/login" style="display:inline-block; text-align:left;">
                <input type="hidden" name="csrf_token" value="{token}">
                Логин: <input type="text" name="username" required><br><br>
                Пароль: <input type="password" name="password" required><br><br>
                <input type="submit" value="Войти">
            </form>
        </body></html>
        """
    
    # Если вошел - показываем записи
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC", (session['user_id'],))
    notes = c.fetchall()
    conn.close()
    
    token = get_csrf_token()
    html_content = f"""
    <html><body style="font-family: Arial; padding: 20px; background:#f9f9f9;">
        <div style="display:flex; justify-content:space-between;">
            <h1>📖 Дневник пользователя: {html.escape(session['username'])}</h1>
            <a href="/logout">Выйти</a>
        </div>
        <hr>
        <h3>Добавить запись:</h3>
        <form method="POST" action="/add_note">
            <input type="hidden" name="csrf_token" value="{token}">
            <textarea name="content" rows="3" cols="50" required placeholder="Ваши мысли..."></textarea><br>
            <input type="submit" value="Сохранить">
        </form>
        <hr>
        <h3>Мои записи:</h3>
    """
    
    if not notes:
        html_content += "<p>Записей пока нет. Напишите первую!</p>"
        
    for note in notes:
        # 🛡️ Защита от XSS (html.escape)
        safe_content = html.escape(note[2])
        html_content += f"""
        <div style="background:white; padding:15px; margin:10px 0; border-left:4px solid #007bff;">
            <p style="margin:0;">{safe_content}</p>
            <small style="color:gray;">{note[3]}</small>
            <br><a href="/delete/{note[0]}" style="color:red; font-size:12px;">Удалить</a>
        </div>
        """
        
    html_content += "</body></html>"
    return html_content

# --- РЕГИСТРАЦИЯ ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        check_csrf()
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            # 🛡️ Защита от SQLi
            c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            return "Ошибка: Пользователь с таким именем уже существует. <a href='/register'>Назад</a>"
        finally:
            conn.close()
            
    token = get_csrf_token()
    return f"""
    <html><body style="font-family: Arial; padding: 40px; text-align: center;">
        <h2>Регистрация</h2>
        <form method="POST" style="display:inline-block; text-align:left;">
            <input type="hidden" name="csrf_token" value="{token}">
            Логин: <input type="text" name="username" required><br><br>
            Пароль: <input type="password" name="password" required><br><br>
            <input type="submit" value="Создать аккаунт">
        </form>
        <p><a href="/">На главную</a></p>
    </body></html>
    """

# --- ВХОД ---
@app.route('/login', methods=['POST'])
def login():
    check_csrf()
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    # 🛡️ Сверка хешей
    if user and check_password_hash(user[1], password):
        session['user_id'] = user[0]
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return "Неверный логин или пароль. <a href='/'>Назад</a>"

# --- ДОБАВЛЕНИЕ ЗАПИСИ ---
@app.route('/add_note', methods=['POST'])
def add_note():
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    check_csrf()
    content = request.form['content']
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # 🛡️ Защита от SQLi
    c.execute("INSERT INTO notes (user_id, content, date) VALUES (?, ?, datetime('now'))", 
              (session['user_id'], content))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- УДАЛЕНИЕ ЗАПИСИ ---
@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # 🛡️ Проверка: удалять можно только СВОИ записи (user_id = ?)
    c.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, session['user_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- ВЫХОД ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    print("Секретный дневник запущен!")
    app.run(host='0.0.0.0', port=5000)
