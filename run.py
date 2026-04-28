"""
個人記帳簿系統 — 啟動入口

使用方式：
    python run.py
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
