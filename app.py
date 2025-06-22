
from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
PASSWORD = "20020230"

def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('diary'))
        else:
            return render_template('login.html', error="密码错误")
    return render_template('login.html')

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = sqlite3.connect('messages.db')
    c = conn.cursor()

    if request.method == 'POST':
        content = request.form.get('content')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO diary (content, timestamp) VALUES (?, ?)", (content, timestamp))
        conn.commit()

    c.execute("SELECT content, timestamp FROM diary ORDER BY id DESC")
    entries = c.fetchall()
    conn.close()
    return render_template('diary.html', entries=entries)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
