import sys
import os

# 添加项目路径到系统路径
path = '/home/yourusername/online_diary'  # 请替换为您的实际用户名
if path not in sys.path:
    sys.path.append(path)

from app import app as application

if __name__ == "__main__":
    application.run() 