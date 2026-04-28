"""
收支紀錄路由模組

負責處理收支紀錄的新增、查詢、編輯、刪除與支出分析等路由。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash

transaction_bp = Blueprint('transaction', __name__)


# ------------------------------------------------------------------
# 新增
# ------------------------------------------------------------------

@transaction_bp.route('/transactions/new')
def new():
    """
    新增收支表單頁面

    顯示新增收入/支出的表單，預先載入分類列表。

    輸入：Query 參數 type（可選，預設 'expense'）用來預選收支類型
    處理邏輯：
        1. 呼叫 Category.get_by_type('expense') 取得支出分類
        2. 呼叫 Category.get_by_type('income') 取得收入分類

    渲染模板：templates/form.html
    傳入變數：categories_expense, categories_income, transaction=None
    """
    # TODO: 實作邏輯
    pass


@transaction_bp.route('/transactions', methods=['POST'])
def create():
    """
    建立收支紀錄

    接收表單資料，驗證後寫入資料庫。

    輸入（表單欄位）：
        - type: 'income' 或 'expense'（必填）
        - amount: 金額，REAL > 0（必填）
        - category_id: 分類 ID，INTEGER（必填）
        - date: 交易日期，YYYY-MM-DD（必填）
        - note: 備註（選填）

    處理邏輯：
        1. 驗證表單欄位合法性
        2. 呼叫 Transaction.create(type, amount, category_id, date, note)
        3. flash('新增成功')
        4. 重導向至首頁 /

    錯誤處理：
        - 驗證失敗 → flash 錯誤訊息，重新渲染表單
    """
    # TODO: 實作邏輯
    pass


# ------------------------------------------------------------------
# 查詢
# ------------------------------------------------------------------

@transaction_bp.route('/transactions')
def history():
    """
    歷史紀錄列表

    顯示所有收支紀錄，支援依月份篩選。

    輸入：Query 參數 month（可選，格式 'YYYY-MM'）
    處理邏輯：
        1. 讀取 month 參數
        2. 呼叫 Transaction.get_all(month=month) 取得紀錄列表

    渲染模板：templates/history.html
    傳入變數：transactions, current_month
    """
    # TODO: 實作邏輯
    pass


# ------------------------------------------------------------------
# 編輯
# ------------------------------------------------------------------

@transaction_bp.route('/transactions/<int:id>/edit')
def edit(id):
    """
    編輯收支表單頁面

    顯示指定紀錄的編輯表單（複用新增表單模板）。

    輸入：URL 參數 id — 要編輯的紀錄 ID
    處理邏輯：
        1. 呼叫 Transaction.get_by_id(id) 取得紀錄
        2. 呼叫 Category.get_by_type('expense') 與 Category.get_by_type('income')

    渲染模板：templates/form.html
    傳入變數：transaction, categories_expense, categories_income

    錯誤處理：
        - 找不到紀錄 → abort(404)
    """
    # TODO: 實作邏輯
    pass


@transaction_bp.route('/transactions/<int:id>/update', methods=['POST'])
def update(id):
    """
    更新收支紀錄

    接收編輯表單資料，驗證後更新資料庫。

    輸入：URL 參數 id + 表單欄位（同 create）
    處理邏輯：
        1. 驗證表單欄位合法性
        2. 呼叫 Transaction.update(id, type, amount, category_id, date, note)
        3. flash('更新成功')
        4. 重導向至歷史紀錄頁 /transactions

    錯誤處理：
        - 找不到紀錄 → abort(404)
        - 驗證失敗 → flash 錯誤訊息，重新渲染編輯表單
    """
    # TODO: 實作邏輯
    pass


# ------------------------------------------------------------------
# 刪除
# ------------------------------------------------------------------

@transaction_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除收支紀錄

    刪除指定的收支紀錄後重導向。

    輸入：URL 參數 id — 要刪除的紀錄 ID
    處理邏輯：
        1. 呼叫 Transaction.get_by_id(id) 確認紀錄存在
        2. 呼叫 Transaction.delete(id)
        3. flash('刪除成功')
        4. 重導向至歷史紀錄頁 /transactions

    錯誤處理：
        - 找不到紀錄 → abort(404)
    """
    # TODO: 實作邏輯
    pass


# ------------------------------------------------------------------
# 分析
# ------------------------------------------------------------------

@transaction_bp.route('/analysis')
def analysis():
    """
    支出分析頁面

    顯示支出統計圖表（圓餅圖/長條圖），支援月份篩選。

    輸入：Query 參數 month（可選，格式 'YYYY-MM'，預設為當月）
    處理邏輯：
        1. 讀取 month 參數（預設當月）
        2. 呼叫 Transaction.get_expense_by_category(month=month) 取得分類統計
        3. 呼叫 Transaction.get_monthly_summary(month=month) 取得月度摘要

    渲染模板：templates/analysis.html
    傳入變數：expense_data, summary, current_month
    """
    # TODO: 實作邏輯
    pass
