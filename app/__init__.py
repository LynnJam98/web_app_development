"""
個人記帳簿系統 — Flask 應用初始化模組

負責建立 Flask 應用實例、設定組態、註冊藍圖，並在首次啟動時初始化資料庫。
"""

import os

from flask import Flask


def create_app():
    """
    Flask 應用工廠函式。

    建立並設定 Flask 應用：
        1. 載入組態（SECRET_KEY 等）
        2. 初始化資料庫（建表與預設資料）
        3. 註冊路由藍圖（main_bp, transaction_bp）

    Returns:
        Flask: 已設定完成的 Flask 應用實例。
    """
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static',
    )

    # 組態設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # 初始化資料庫
    from app.models import init_db
    init_db()

    # 註冊藍圖
    from app.routes.main import main_bp
    from app.routes.transaction import transaction_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(transaction_bp)

    return app
