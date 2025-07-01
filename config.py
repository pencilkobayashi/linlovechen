import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key_here"  # Flask session 密钥
    
    @staticmethod
    def load_password():
        """从文件中读取密码"""
        password_file = 'password.txt'
        if os.path.exists(password_file):
            with open(password_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        return "20020230"  # 默认密码
    
    @staticmethod
    def save_password(new_password):
        """保存新密码到文件"""
        password_file = 'password.txt'
        with open(password_file, 'w', encoding='utf-8') as f:
            f.write(new_password)
    
    @property
    def PASSWORD(self):
        return self.load_password()