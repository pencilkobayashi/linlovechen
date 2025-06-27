from flask import Flask, render_template, request, redirect, url_for, session, g
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.before_request
def check_login():
    """全局登录检查：排除登录页和静态文件"""
    exempted_routes = ['login', 'static']
    if not session.get('logged_in') and request.endpoint not in exempted_routes:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == app.config['PASSWORD']:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = "密码错误！请重试。"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('protected.html')

@app.route('/another-page')
def another_page():
    return render_template('protected.html')

if __name__ == '__main__':
    app.run(debug=True)