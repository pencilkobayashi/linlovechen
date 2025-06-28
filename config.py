import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key_here"  # Flask session 密钥
    PASSWORD = "20020230"  # 全局密码（生产环境建议用环境变量）