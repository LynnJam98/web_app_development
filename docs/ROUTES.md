# 路由設計文件 (Routes) - 個人記帳簿系統

本文件根據 `docs/PRD.md`、`docs/ARCHITECTURE.md` 與 `docs/DB_DESIGN.md`，規劃所有 Flask 路由的 URL、HTTP 方法、對應模板與處理邏輯。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁（當月總覽） | GET | `/` | `templates/index.html` | 顯示當月總收入、總支出、結餘與近期紀錄 |
| 新增收支表單 | GET | `/transactions/new` | `templates/form.html` | 顯示新增收入/支出的表單 |
| 建立收支紀錄 | POST | `/transactions` | — | 接收表單資料，存入 DB，重導向至首頁 |
| 歷史紀錄列表 | GET | `/transactions` | `templates/history.html` | 顯示所有收支紀錄，支援月份篩選 |
| 編輯收支表單 | GET | `/transactions/<id>/edit` | `templates/form.html` | 顯示指定紀錄的編輯表單（複用新增表單） |
| 更新收支紀錄 | POST | `/transactions/<id>/update` | — | 接收編輯表單，更新 DB，重導向至歷史紀錄 |
| 刪除收支紀錄 | POST | `/transactions/<id>/delete` | — | 刪除指定紀錄，重導向至歷史紀錄 |
| 支出分析 | GET | `/analysis` | `templates/analysis.html` | 顯示支出統計圖表（支援月份篩選） |

---

## 2. 每個路由的詳細說明

### 2-1. 首頁（當月總覽）

- **URL**：`GET /`
- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `Transaction.get_monthly_summary()` 取得當月總收入、總支出與結餘
  2. 呼叫 `Transaction.get_recent(limit=10)` 取得近期 10 筆紀錄
- **輸出**：渲染 `templates/index.html`，傳入 `summary` 與 `recent_transactions`
- **錯誤處理**：無特殊錯誤情境

---

### 2-2. 新增收支表單

- **URL**：`GET /transactions/new`
- **輸入**：Query 參數 `type`（可選，預設 `expense`），用來預選收入/支出
- **處理邏輯**：
  1. 呼叫 `Category.get_by_type('expense')` 與 `Category.get_by_type('income')` 取得分類列表
- **輸出**：渲染 `templates/form.html`，傳入 `categories_expense`、`categories_income` 與 `transaction=None`（表示新增模式）
- **錯誤處理**：無特殊錯誤情境

---

### 2-3. 建立收支紀錄

- **URL**：`POST /transactions`
- **輸入**：表單欄位
  - `type`（TEXT，必填）：`income` 或 `expense`
  - `amount`（REAL，必填）：金額（前端已經過四則運算）
  - `category_id`（INTEGER，必填）：分類 ID
  - `date`（TEXT，必填）：交易日期（YYYY-MM-DD）
  - `note`（TEXT，選填）：備註
- **處理邏輯**：
  1. 驗證表單欄位（type、amount、category_id、date 是否合法）
  2. 呼叫 `Transaction.create(type, amount, category_id, date, note)`
  3. 重導向至首頁 `/`
- **錯誤處理**：
  - 驗證失敗 → 重新渲染表單頁面並顯示錯誤訊息（使用 `flash()`）
  - 金額不合法（≤ 0 或非數字）→ 提示「請輸入有效金額」

---

### 2-4. 歷史紀錄列表

- **URL**：`GET /transactions`
- **輸入**：Query 參數 `month`（可選，格式 `YYYY-MM`），用來篩選月份
- **處理邏輯**：
  1. 若有 `month` 參數，呼叫 `Transaction.get_all(month=month)`
  2. 若無，呼叫 `Transaction.get_all()` 取得全部紀錄
- **輸出**：渲染 `templates/history.html`，傳入 `transactions` 與 `current_month`
- **錯誤處理**：無特殊錯誤情境

---

### 2-5. 編輯收支表單

- **URL**：`GET /transactions/<id>/edit`
- **輸入**：URL 參數 `id`（INTEGER）— 要編輯的紀錄 ID
- **處理邏輯**：
  1. 呼叫 `Transaction.get_by_id(id)` 取得紀錄
  2. 呼叫 `Category.get_by_type('expense')` 與 `Category.get_by_type('income')` 取得分類列表
- **輸出**：渲染 `templates/form.html`（複用新增表單），傳入 `transaction`（表示編輯模式）、`categories_expense`、`categories_income`
- **錯誤處理**：
  - 找不到紀錄（`id` 不存在）→ 回傳 404 頁面

---

### 2-6. 更新收支紀錄

- **URL**：`POST /transactions/<id>/update`
- **輸入**：URL 參數 `id` + 表單欄位（同建立）
- **處理邏輯**：
  1. 驗證表單欄位
  2. 呼叫 `Transaction.update(id, type, amount, category_id, date, note)`
  3. 重導向至歷史紀錄頁 `/transactions`
- **錯誤處理**：
  - 找不到紀錄 → 回傳 404
  - 驗證失敗 → 重新渲染編輯表單並顯示錯誤訊息

---

### 2-7. 刪除收支紀錄

- **URL**：`POST /transactions/<id>/delete`
- **輸入**：URL 參數 `id`（INTEGER）— 要刪除的紀錄 ID
- **處理邏輯**：
  1. 呼叫 `Transaction.get_by_id(id)` 確認紀錄存在
  2. 呼叫 `Transaction.delete(id)`
  3. 重導向至歷史紀錄頁 `/transactions`
- **錯誤處理**：
  - 找不到紀錄 → 回傳 404

---

### 2-8. 支出分析

- **URL**：`GET /analysis`
- **輸入**：Query 參數 `month`（可選，格式 `YYYY-MM`），預設為當月
- **處理邏輯**：
  1. 呼叫 `Transaction.get_expense_by_category(month=month)` 取得各分類支出統計
  2. 呼叫 `Transaction.get_monthly_summary(month=month)` 取得月度摘要
- **輸出**：渲染 `templates/analysis.html`，傳入 `expense_data`、`summary` 與 `current_month`
- **錯誤處理**：無特殊錯誤情境

---

## 3. Jinja2 模板清單

所有模板皆繼承 `base.html` 共用排版。

| 模板檔案 | 繼承 | 說明 |
| --- | --- | --- |
| `templates/base.html` | — | 共用排版：HTML head、導覽列 (Navbar)、Footer、Flash 訊息 |
| `templates/index.html` | `base.html` | 首頁：當月收支摘要卡片 + 近期紀錄列表 |
| `templates/form.html` | `base.html` | 新增/編輯共用表單：類型切換、金額（含計算機）、分類、日期、備註 |
| `templates/history.html` | `base.html` | 歷史紀錄：月份篩選器 + 收支紀錄表格（含編輯/刪除按鈕） |
| `templates/analysis.html` | `base.html` | 支出分析：月份選擇器 + Chart.js 圓餅圖/長條圖 |

---

## 4. 路由骨架程式碼

路由骨架位於 `app/routes/` 資料夾：

- `app/routes/__init__.py` — 路由藍圖初始化
- `app/routes/main.py` — 首頁路由
- `app/routes/transaction.py` — 收支紀錄相關路由（CRUD + 分析）
