"""
Category Model — 分類資料表操作

負責對 categories 資料表進行 CRUD 操作。
"""

from app.models import get_db


class Category:
    """分類 Model，提供分類資料的查詢方法。"""

    @staticmethod
    def get_all():
        """
        取得所有分類。

        Returns:
            list[sqlite3.Row]: 所有分類的列表。
        """
        conn = get_db()
        try:
            rows = conn.execute(
                'SELECT * FROM categories ORDER BY type, id'
            ).fetchall()
            return rows
        finally:
            conn.close()

    @staticmethod
    def get_by_id(category_id):
        """
        依 ID 取得單一分類。

        Args:
            category_id (int): 分類 ID。

        Returns:
            sqlite3.Row | None: 分類資料，若不存在則回傳 None。
        """
        conn = get_db()
        try:
            row = conn.execute(
                'SELECT * FROM categories WHERE id = ?',
                (category_id,)
            ).fetchone()
            return row
        finally:
            conn.close()

    @staticmethod
    def get_by_type(category_type):
        """
        依類型取得分類列表。

        Args:
            category_type (str): 分類類型，'income' 或 'expense'。

        Returns:
            list[sqlite3.Row]: 符合類型的分類列表。
        """
        conn = get_db()
        try:
            rows = conn.execute(
                'SELECT * FROM categories WHERE type = ? ORDER BY id',
                (category_type,)
            ).fetchall()
            return rows
        finally:
            conn.close()

    @staticmethod
    def create(name, category_type):
        """
        新增一筆分類。

        Args:
            name (str): 分類名稱。
            category_type (str): 分類類型，'income' 或 'expense'。

        Returns:
            int: 新建立的分類 ID。
        """
        conn = get_db()
        try:
            cursor = conn.execute(
                'INSERT INTO categories (name, type) VALUES (?, ?)',
                (name, category_type)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def update(category_id, name, category_type):
        """
        更新一筆分類。

        Args:
            category_id (int): 分類 ID。
            name (str): 新的分類名稱。
            category_type (str): 新的分類類型。
        """
        conn = get_db()
        try:
            conn.execute(
                'UPDATE categories SET name = ?, type = ? WHERE id = ?',
                (name, category_type, category_id)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(category_id):
        """
        刪除一筆分類。

        Args:
            category_id (int): 要刪除的分類 ID。
        """
        conn = get_db()
        try:
            conn.execute(
                'DELETE FROM categories WHERE id = ?',
                (category_id,)
            )
            conn.commit()
        finally:
            conn.close()
