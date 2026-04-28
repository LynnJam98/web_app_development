-- ============================================
-- 個人記帳簿系統 - SQLite 建表語法
-- ============================================

-- 分類資料表
CREATE TABLE IF NOT EXISTS categories (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    type       TEXT    NOT NULL CHECK (type IN ('income', 'expense')),
    created_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 收支紀錄資料表
CREATE TABLE IF NOT EXISTS transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    type        TEXT    NOT NULL CHECK (type IN ('income', 'expense')),
    amount      REAL    NOT NULL CHECK (amount > 0),
    category_id INTEGER NOT NULL,
    date        TEXT    NOT NULL DEFAULT (date('now', 'localtime')),
    note        TEXT    DEFAULT '',
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

-- 建立索引：加速依日期查詢
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions (date);

-- 建立索引：加速依類型查詢
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions (type);

-- ============================================
-- 預設分類資料
-- ============================================

-- 支出分類
INSERT OR IGNORE INTO categories (id, name, type) VALUES (1,  '餐飲', 'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (2,  '交通', 'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (3,  '購物', 'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (4,  '娛樂', 'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (5,  '居住', 'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (6,  '醫療', 'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (7,  '教育', 'expense');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (8,  '其他支出', 'expense');

-- 收入分類
INSERT OR IGNORE INTO categories (id, name, type) VALUES (9,  '薪資', 'income');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (10, '獎金', 'income');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (11, '投資', 'income');
INSERT OR IGNORE INTO categories (id, name, type) VALUES (12, '其他收入', 'income');
