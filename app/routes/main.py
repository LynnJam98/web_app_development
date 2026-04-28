"""
主頁路由模組

負責處理首頁（當月總覽）的顯示邏輯。
"""

from flask import Blueprint, render_template

from app.models.transaction import Transaction

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    首頁 — 當月總覽

    顯示當月總收入、總支出、結餘，以及最近 10 筆收支紀錄。

    處理邏輯：
        1. 呼叫 Transaction.get_monthly_summary() 取得當月收支摘要
        2. 呼叫 Transaction.get_recent(limit=10) 取得近期紀錄

    渲染模板：templates/index.html
    傳入變數：summary, recent_transactions
    """
    summary = Transaction.get_monthly_summary()
    recent_transactions = Transaction.get_recent(limit=10)

    return render_template(
        'index.html',
        summary=summary,
        recent_transactions=recent_transactions,
    )
