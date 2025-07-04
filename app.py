from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
from config import Config
import json
import os
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='/static')
config = Config()
app.config.from_object(config)

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
        if request.form['password'] == config.PASSWORD:
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
    return render_template('index.html')

@app.route('/notes')
def notes_list():
    """查看所有日记列表"""
    notes = load_notes()
    return render_template('notes_list.html', notes=notes)

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    """更改密码"""
    error = None
    success = None
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # 验证当前密码
        if current_password != config.PASSWORD:
            error = "当前密码错误！"
        elif not new_password:
            error = "新密码不能为空！"
        elif len(new_password) < 6:
            error = "新密码长度至少6位！"
        elif new_password != confirm_password:
            error = "两次输入的新密码不一致！"
        else:
            # 保存新密码
            try:
                Config.save_password(new_password)
                success = "密码修改成功！"
            except Exception as e:
                error = f"密码保存失败：{str(e)}"
    
    return render_template('change_password.html', error=error, success=success)

@app.route('/another-page')
def another_page():
    return render_template('protected.html')

# 日记数据文件路径
NOTES_FILE = 'notes.json'

def load_notes():
    """加载日记数据"""
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_notes(notes):
    """保存日记数据"""
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

@app.route('/api/notes', methods=['GET'])
def get_notes():
    """获取所有日记"""
    notes = load_notes()
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def add_note():
    """添加新日记"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效的请求数据'}), 400
        
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'error': '日记内容不能为空'}), 400
    
    notes = load_notes()
    new_note = {
        'id': len(notes) + 1,
        'content': content,
        'created_at': datetime.now().isoformat()
    }
    notes.append(new_note)
    save_notes(notes)
    
    return jsonify(new_note)

if __name__ == '__main__':
    app.run(debug=True)