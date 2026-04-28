"""
Transaction Model — 收支紀錄資料表操作

負責對 transactions 資料表進行 CRUD 操作，以及提供統計查詢方法。
使用 sqlite3 模組，資料庫路徑為 instance/database.db。
"""

import sqlite3
from datetime import date, datetime

from app.models import get_db


class Transaction:
    """收支紀錄 Model，提供收支資料的 CRUD 與統計方法。"""

    # ------------------------------------------------------------------
    # CRUD 方法
    # ------------------------------------------------------------------

    @staticmethod
    def create(trans_type, amount, category_id, trans_date=None, note=''):
        """
        新增一筆收支紀錄。

        Args:
            trans_type (str): 收支類型，'income' 或 'expense'。
            amount (float): 金額（必須大於 0）。
            category_id (int): 分類 ID。
            trans_date (str, optional): 交易日期（YYYY-MM-DD），預設為今日。
            note (str, optional): 備註，預設為空字串。

        Returns:
            int | None: 新建立的紀錄 ID，失敗時回傳 None。
        """
        if trans_date is None:
            trans_date = date.today().isoformat()

        try:
            conn = get_db()
            cursor = conn.execute(
                '''INSERT INTO transactions (type, amount, category_id, date, note)
                   VALUES (?, ?, ?, ?, ?)''',
                (trans_type, amount, category_id, trans_date, note)
            )
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
        except sqlite3.Error as e:
            print(f"[Transaction ERROR] create 失敗: {e}")
            return None

    @staticmethod
    def get_all(month=None):
        """
        取得所有收支紀錄，可選依月份篩選。

        Args:
            month (str, optional): 月份篩選（格式：'YYYY-MM'）。

        Returns:
            list[sqlite3.Row]: 收支紀錄列表，按日期降序排列。
            空列表: 查詢失敗時回傳空列表。
        """
        try:
            conn = get_db()
            if month:
                rows = conn.execute(
                    '''SELECT t.*, c.name as category_name
                       FROM transactions t
                       JOIN categories c ON t.category_id = c.id
                       WHERE strftime('%Y-%m', t.date) = ?
                       ORDER BY t.date DESC, t.id DESC''',
                    (month,)
                ).fetchall()
            else:
                rows = conn.execute(
                    '''SELECT t.*, c.name as category_name
                       FROM transactions t
                       JOIN categories c ON t.category_id = c.id
                       ORDER BY t.date DESC, t.id DESC'''
                ).fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print(f"[Transaction ERROR] get_all 失敗: {e}")
            return []

    @staticmethod
    def get_by_id(transaction_id):
        """
        依 ID 取得單一收支紀錄。

        Args:
            transaction_id (int): 紀錄 ID。

        Returns:
            sqlite3.Row | None: 紀錄資料，若不存在或查詢失敗則回傳 None。
        """
        try:
            conn = get_db()
            row = conn.execute(
                '''SELECT t.*, c.name as category_name
                   FROM transactions t
                   JOIN categories c ON t.category_id = c.id
                   WHERE t.id = ?''',
                (transaction_id,)
            ).fetchone()
            conn.close()
            return row
        except sqlite3.Error as e:
            print(f"[Transaction ERROR] get_by_id({transaction_id}) 失敗: {e}")
            return None

    @staticmethod
    def update(transaction_id, trans_type, amount, category_id, trans_date, note=''):
        """
        更新一筆收支紀錄。

        Args:
            transaction_id (int): 紀錄 ID。
            trans_type (str): 收支類型，'income' 或 'expense'。
            amount (float): 金額。
            category_id (int): 分類 ID。
            trans_date (str): 交易日期（YYYY-MM-DD）。
            note (str, optional): 備註，預設為空字串。

        Returns:
            bool: 更新成功回傳 True，失敗回傳 False。
        """
        now = datetime.now().isoformat(timespec='seconds')
        try:
            conn = get_db()
            conn.execute(
                '''UPDATE transactions
                   SET type = ?, amount = ?, category_id = ?, date = ?, note = ?, updated_at = ?
                   WHERE id = ?''',
                (trans_type, amount, category_id, trans_date, note, now, transaction_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"[Transaction ERROR] update({transaction_id}) 失敗: {e}")
            return False

    @staticmethod
    def delete(transaction_id):
        """
        刪除一筆收支紀錄。

        Args:
            transaction_id (int): 要刪除的紀錄 ID。

        Returns:
            bool: 刪除成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db()
            conn.execute(
                'DELETE FROM transactions WHERE id = ?',
                (transaction_id,)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"[Transaction ERROR] delete({transaction_id}) 失敗: {e}")
            return False

    # ------------------------------------------------------------------
    # 統計查詢方法
    # ------------------------------------------------------------------

    @staticmethod
    def get_monthly_summary(month=None):
        """
        取得指定月份的收支摘要（總收入、總支出、結餘）。

        Args:
            month (str, optional): 月份（格式：'YYYY-MM'），預設為當月。

        Returns:
            dict: 包含 'total_income', 'total_expense', 'balance' 的字典。
                  查詢失敗時各值皆為 0。
        """
        if month is None:
            month = date.today().strftime('%Y-%m')

        try:
            conn = get_db()
            row = conn.execute(
                '''SELECT
                     COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) as total_income,
                     COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) as total_expense
                   FROM transactions
                   WHERE strftime('%Y-%m', date) = ?''',
                (month,)
            ).fetchone()
            conn.close()

            total_income = row['total_income']
            total_expense = row['total_expense']

            return {
                'total_income': total_income,
                'total_expense': total_expense,
                'balance': total_income - total_expense,
            }
        except sqlite3.Error as e:
            print(f"[Transaction ERROR] get_monthly_summary({month}) 失敗: {e}")
            return {'total_income': 0, 'total_expense': 0, 'balance': 0}

    @staticmethod
    def get_expense_by_category(month=None):
        """
        取得指定月份各分類的支出統計（用於圓餅圖/長條圖）。

        Args:
            month (str, optional): 月份（格式：'YYYY-MM'），預設為當月。

        Returns:
            list[sqlite3.Row]: 包含 'category_name' 與 'total' 的統計列表。
            空列表: 查詢失敗時回傳空列表。
        """
        if month is None:
            month = date.today().strftime('%Y-%m')

        try:
            conn = get_db()
            rows = conn.execute(
                '''SELECT c.name as category_name, SUM(t.amount) as total
                   FROM transactions t
                   JOIN categories c ON t.category_id = c.id
                   WHERE t.type = 'expense' AND strftime('%Y-%m', t.date) = ?
                   GROUP BY t.category_id
                   ORDER BY total DESC''',
                (month,)
            ).fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print(f"[Transaction ERROR] get_expense_by_category({month}) 失敗: {e}")
            return []

    @staticmethod
    def get_recent(limit=10):
        """
        取得最近的收支紀錄。

        Args:
            limit (int): 回傳的筆數上限，預設為 10。

        Returns:
            list[sqlite3.Row]: 最近的收支紀錄列表。
            空列表: 查詢失敗時回傳空列表。
        """
        try:
            conn = get_db()
            rows = conn.execute(
                '''SELECT t.*, c.name as category_name
                   FROM transactions t
                   JOIN categories c ON t.category_id = c.id
                   ORDER BY t.date DESC, t.id DESC
                   LIMIT ?''',
                (limit,)
            ).fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print(f"[Transaction ERROR] get_recent({limit}) 失敗: {e}")
            return []
