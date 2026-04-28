"""
Category Model — 分類資料表操作

負責對 categories 資料表進行 CRUD 操作。
使用 sqlite3 模組，資料庫路徑為 instance/database.db。
"""

import sqlite3

from app.models import get_db


class Category:
    """分類 Model，提供分類資料的 CRUD 方法。"""

    @staticmethod
    def get_all():
        """
        取得所有分類，依類型與 ID 排序。

        Returns:
            list[sqlite3.Row]: 所有分類的列表。
            空列表: 查詢失敗時回傳空列表。
        """
        try:
            conn = get_db()
            rows = conn.execute(
                'SELECT * FROM categories ORDER BY type, id'
            ).fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print(f"[Category ERROR] get_all 失敗: {e}")
            return []

    @staticmethod
    def get_by_id(category_id):
        """
        依 ID 取得單一分類。

        Args:
            category_id (int): 分類 ID。

        Returns:
            sqlite3.Row | None: 分類資料，若不存在或查詢失敗則回傳 None。
        """
        try:
            conn = get_db()
            row = conn.execute(
                'SELECT * FROM categories WHERE id = ?',
                (category_id,)
            ).fetchone()
            conn.close()
            return row
        except sqlite3.Error as e:
            print(f"[Category ERROR] get_by_id({category_id}) 失敗: {e}")
            return None

    @staticmethod
    def get_by_type(category_type):
        """
        依類型取得分類列表（income 或 expense）。

        Args:
            category_type (str): 分類類型，'income' 或 'expense'。

        Returns:
            list[sqlite3.Row]: 符合類型的分類列表。
            空列表: 查詢失敗時回傳空列表。
        """
        try:
            conn = get_db()
            rows = conn.execute(
                'SELECT * FROM categories WHERE type = ? ORDER BY id',
                (category_type,)
            ).fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print(f"[Category ERROR] get_by_type({category_type}) 失敗: {e}")
            return []

    @staticmethod
    def create(name, category_type):
        """
        新增一筆分類。

        Args:
            name (str): 分類名稱。
            category_type (str): 分類類型，'income' 或 'expense'。

        Returns:
            int | None: 新建立的分類 ID，失敗時回傳 None。
        """
        try:
            conn = get_db()
            cursor = conn.execute(
                'INSERT INTO categories (name, type) VALUES (?, ?)',
                (name, category_type)
            )
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
        except sqlite3.Error as e:
            print(f"[Category ERROR] create({name}, {category_type}) 失敗: {e}")
            return None

    @staticmethod
    def update(category_id, name, category_type):
        """
        更新一筆分類。

        Args:
            category_id (int): 分類 ID。
            name (str): 新的分類名稱。
            category_type (str): 新的分類類型。

        Returns:
            bool: 更新成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db()
            conn.execute(
                'UPDATE categories SET name = ?, type = ? WHERE id = ?',
                (name, category_type, category_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"[Category ERROR] update({category_id}) 失敗: {e}")
            return False

    @staticmethod
    def delete(category_id):
        """
        刪除一筆分類。

        Args:
            category_id (int): 要刪除的分類 ID。

        Returns:
            bool: 刪除成功回傳 True，失敗回傳 False。
        """
        try:
            conn = get_db()
            conn.execute(
                'DELETE FROM categories WHERE id = ?',
                (category_id,)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"[Category ERROR] delete({category_id}) 失敗: {e}")
            return False
