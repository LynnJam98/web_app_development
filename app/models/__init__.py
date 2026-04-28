"""
資料庫連線初始化模組

負責建立與管理 SQLite 資料庫連線，並在首次啟動時自動執行建表語法。
"""

import os
import sqlite3

# 資料庫檔案路徑（位於 instance/ 資料夾）
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')


def get_db():
    """
    取得資料庫連線。

    回傳一個 sqlite3 連線物件，設定 row_factory 為 sqlite3.Row，
    讓查詢結果可以用欄位名稱存取（如 row['amount']）。

    Returns:
        sqlite3.Connection: 資料庫連線物件。

    Raises:
        sqlite3.Error: 無法連線至資料庫時拋出。
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")  # 啟用外鍵約束
        return conn
    except sqlite3.Error as e:
        print(f"[DB ERROR] 無法連線至資料庫: {e}")
        raise


def init_db():
    """
    初始化資料庫。

    如果 instance/ 資料夾不存在，會自動建立。
    接著讀取 database/schema.sql 並執行建表語法與預設資料。

    Raises:
        FileNotFoundError: 找不到 schema.sql 時拋出。
        sqlite3.Error: 執行 SQL 失敗時拋出。
    """
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    try:
        conn = get_db()
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("[DB] 資料庫初始化完成。")
    except FileNotFoundError:
        print(f"[DB ERROR] 找不到 schema 檔案: {SCHEMA_PATH}")
        raise
    except sqlite3.Error as e:
        print(f"[DB ERROR] 資料庫初始化失敗: {e}")
        raise
