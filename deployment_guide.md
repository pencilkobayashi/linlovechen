# PythonAnywhere 部署指南 💕

## 步骤1: 上传文件
1. 将所有项目文件上传到 `/home/yourusername/online_diary/` 目录
2. 确保目录结构如下：
```
/home/yourusername/online_diary/
├── app.py
├── wsgi.py
├── config.py
├── requirements.txt
├── static/
│   ├── style.css
│   ├── script.js
│   └── OIP.jpg
└── templates/
    ├── index.html
    ├── login.html
    ├── notes_list.html
    └── protected.html
```

## 步骤2: 修改wsgi.py
在 `wsgi.py` 文件中，将路径改为您的实际用户名：
```python
path = '/home/YOUR_USERNAME/online_diary'  # 替换YOUR_USERNAME
```

## 步骤3: Web应用配置
在PythonAnywhere的Web选项卡中：

1. **Source code**: `/home/yourusername/online_diary`
2. **Working directory**: `/home/yourusername/online_diary`
3. **WSGI configuration file**: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

## 步骤4: 静态文件映射 🎨 (重要！这是粉色样式的关键)
在Web选项卡的"Static files"部分添加：

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/online_diary/static/` |

## 步骤5: 安装依赖
在PythonAnywhere的Bash控制台中运行：
```bash
cd ~/online_diary
pip3.10 install --user -r requirements.txt
```

## 步骤6: 重新加载Web应用
点击Web选项卡中的 "Reload yourusername.pythonanywhere.com" 按钮

## 常见问题解决 🔧

### 如果CSS样式还是不显示：
1. 检查静态文件映射是否正确
2. 确保文件权限正确：`chmod 644 static/*`
3. 检查浏览器开发者工具的Network选项卡，看是否有404错误
4. 尝试直接访问：`https://yourusername.pythonanywhere.com/static/style.css`

### 如果还有问题：
1. 在Web选项卡点击 "Error log" 查看错误信息
2. 确保所有文件都上传成功
3. 检查文件编码是否为UTF-8

## 成功标志 💖
部署成功后，您应该看到：
- 粉色渐变背景
- 可爱的小狗装饰
- 圆角按钮和输入框
- 爱心和小爪印动画

享受您和丽君宝宝的专属爱情回忆录吧！💕 