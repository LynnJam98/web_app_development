"""
收支紀錄路由模組

負責處理收支紀錄的新增、查詢、編輯、刪除與支出分析等路由。
使用 Flask Blueprint 組織路由，所有表單驗證失敗時會透過 flash 顯示錯誤訊息。
"""

from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app.models.category import Category
from app.models.transaction import Transaction

transaction_bp = Blueprint('transaction', __name__)


# ------------------------------------------------------------------
# 輔助函式
# ------------------------------------------------------------------

def _validate_form(form):
    """
    驗證收支表單的必填欄位。

    Args:
        form (dict-like): request.form 物件。

    Returns:
        tuple: (errors, data)
            - errors (list[str]): 錯誤訊息列表，空列表表示驗證通過。
            - data (dict): 解析後的表單資料。
    """
    errors = []
    data = {}

    # 類型驗證
    trans_type = form.get('type', '').strip()
    if trans_type not in ('income', 'expense'):
        errors.append('請選擇收支類型（收入或支出）。')
    data['type'] = trans_type

    # 金額驗證
    amount_str = form.get('amount', '').strip()
    if not amount_str:
        errors.append('請輸入金額。')
    else:
        try:
            amount = float(amount_str)
            if amount <= 0:
                errors.append('金額必須大於 0。')
        except ValueError:
            errors.append('請輸入有效的金額數字。')
            amount = 0
    data['amount'] = amount if amount_str else 0

    # 分類驗證
    category_id_str = form.get('category_id', '').strip()
    if not category_id_str:
        errors.append('請選擇分類。')
        data['category_id'] = None
    else:
        try:
            data['category_id'] = int(category_id_str)
        except ValueError:
            errors.append('分類 ID 無效。')
            data['category_id'] = None

    # 日期驗證
    trans_date = form.get('date', '').strip()
    if not trans_date:
        trans_date = date.today().isoformat()
    data['date'] = trans_date

    # 備註（選填）
    data['note'] = form.get('note', '').strip()

    return errors, data


def _get_categories():
    """
    取得收入與支出的分類列表。

    Returns:
        tuple: (categories_expense, categories_income)
    """
    categories_expense = Category.get_by_type('expense')
    categories_income = Category.get_by_type('income')
    return categories_expense, categories_income


# ------------------------------------------------------------------
# 新增
# ------------------------------------------------------------------

@transaction_bp.route('/transactions/new')
def new():
    """
    新增收支表單頁面

    顯示新增收入/支出的表單，預先載入分類列表。

    輸入：Query 參數 type（可選，預設 'expense'）用來預選收支類型
    渲染模板：templates/form.html
    """
    default_type = request.args.get('type', 'expense')
    categories_expense, categories_income = _get_categories()

    return render_template(
        'form.html',
        transaction=None,
        default_type=default_type,
        categories_expense=categories_expense,
        categories_income=categories_income,
        today=date.today().isoformat(),
    )


@transaction_bp.route('/transactions', methods=['POST'])
def create():
    """
    建立收支紀錄

    接收表單資料，驗證後寫入資料庫。
    成功：flash 成功訊息，重導向至首頁。
    失敗：flash 錯誤訊息，重新渲染表單。
    """
    errors, data = _validate_form(request.form)

    if errors:
        for error in errors:
            flash(error, 'danger')
        # 重新渲染表單，保留使用者已輸入的資料
        categories_expense, categories_income = _get_categories()
        return render_template(
            'form.html',
            transaction=None,
            default_type=data.get('type', 'expense'),
            categories_expense=categories_expense,
            categories_income=categories_income,
            today=date.today().isoformat(),
            form_data=data,
        ), 400

    result = Transaction.create(
        trans_type=data['type'],
        amount=data['amount'],
        category_id=data['category_id'],
        trans_date=data['date'],
        note=data['note'],
    )

    if result:
        flash('新增成功！', 'success')
    else:
        flash('新增失敗，請稍後再試。', 'danger')

    return redirect(url_for('main.index'))


# ------------------------------------------------------------------
# 查詢
# ------------------------------------------------------------------

@transaction_bp.route('/transactions')
def history():
    """
    歷史紀錄列表

    顯示所有收支紀錄，支援依月份篩選。

    輸入：Query 參數 month（可選，格式 'YYYY-MM'）
    渲染模板：templates/history.html
    """
    month = request.args.get('month', None)
    current_month = month if month else date.today().strftime('%Y-%m')
    transactions = Transaction.get_all(month=current_month)

    return render_template(
        'history.html',
        transactions=transactions,
        current_month=current_month,
    )


# ------------------------------------------------------------------
# 編輯
# ------------------------------------------------------------------

@transaction_bp.route('/transactions/<int:id>/edit')
def edit(id):
    """
    編輯收支表單頁面

    顯示指定紀錄的編輯表單（複用新增表單模板）。
    找不到紀錄時回傳 404。

    輸入：URL 參數 id — 要編輯的紀錄 ID
    渲染模板：templates/form.html
    """
    transaction = Transaction.get_by_id(id)
    if transaction is None:
        abort(404)

    categories_expense, categories_income = _get_categories()

    return render_template(
        'form.html',
        transaction=transaction,
        default_type=transaction['type'],
        categories_expense=categories_expense,
        categories_income=categories_income,
        today=date.today().isoformat(),
    )


@transaction_bp.route('/transactions/<int:id>/update', methods=['POST'])
def update(id):
    """
    更新收支紀錄

    接收編輯表單資料，驗證後更新資料庫。
    成功：flash 成功訊息，重導向至歷史紀錄頁。
    失敗：flash 錯誤訊息，重新渲染編輯表單。
    """
    transaction = Transaction.get_by_id(id)
    if transaction is None:
        abort(404)

    errors, data = _validate_form(request.form)

    if errors:
        for error in errors:
            flash(error, 'danger')
        categories_expense, categories_income = _get_categories()
        return render_template(
            'form.html',
            transaction=transaction,
            default_type=data.get('type', 'expense'),
            categories_expense=categories_expense,
            categories_income=categories_income,
            today=date.today().isoformat(),
            form_data=data,
        ), 400

    success = Transaction.update(
        transaction_id=id,
        trans_type=data['type'],
        amount=data['amount'],
        category_id=data['category_id'],
        trans_date=data['date'],
        note=data['note'],
    )

    if success:
        flash('更新成功！', 'success')
    else:
        flash('更新失敗，請稍後再試。', 'danger')

    return redirect(url_for('transaction.history'))


# ------------------------------------------------------------------
# 刪除
# ------------------------------------------------------------------

@transaction_bp.route('/transactions/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除收支紀錄

    刪除指定的收支紀錄後重導向至歷史紀錄頁。
    找不到紀錄時回傳 404。

    輸入：URL 參數 id — 要刪除的紀錄 ID
    """
    transaction = Transaction.get_by_id(id)
    if transaction is None:
        abort(404)

    success = Transaction.delete(id)

    if success:
        flash('刪除成功！', 'success')
    else:
        flash('刪除失敗，請稍後再試。', 'danger')

    return redirect(url_for('transaction.history'))


# ------------------------------------------------------------------
# 分析
# ------------------------------------------------------------------

@transaction_bp.route('/analysis')
def analysis():
    """
    支出分析頁面

    顯示支出統計圖表（圓餅圖/長條圖），支援月份篩選。

    輸入：Query 參數 month（可選，格式 'YYYY-MM'，預設為當月）
    渲染模板：templates/analysis.html
    """
    month = request.args.get('month', None)
    current_month = month if month else date.today().strftime('%Y-%m')

    expense_data = Transaction.get_expense_by_category(month=current_month)
    summary = Transaction.get_monthly_summary(month=current_month)

    # 將統計資料轉為圖表所需格式（JSON 序列化用）
    chart_labels = [row['category_name'] for row in expense_data]
    chart_values = [row['total'] for row in expense_data]

    return render_template(
        'analysis.html',
        expense_data=expense_data,
        summary=summary,
        current_month=current_month,
        chart_labels=chart_labels,
        chart_values=chart_values,
    )
