# 流程圖文件 (Flowchart) - 個人記帳簿系統

本文件根據 `docs/PRD.md` 與 `docs/ARCHITECTURE.md`，以 Mermaid 語法呈現使用者操作流程與系統內部資料流動方式。

---

## 1. 使用者流程圖（User Flow）

以下流程圖描述使用者從進入網站開始，可進行的所有主要操作路徑。

```mermaid
flowchart LR
  A([使用者開啟網頁]) --> B[首頁 - 當月總覽]
  B --> C{要執行什麼操作？}

  C -->|新增收支| D[新增收支表單頁面]
  D --> D1[選擇類型：收入 / 支出]
  D1 --> D2[輸入金額 - 支援四則運算]
  D2 --> D3[選擇分類]
  D3 --> D4[選擇日期 - 預設今日]
  D4 --> D5[填寫備註 - 選填]
  D5 --> D6[送出表單]
  D6 --> B

  C -->|查看歷史紀錄| E[歷史紀錄列表]
  E --> E1[依月份篩選紀錄]
  E1 --> E2{對紀錄進行操作？}
  E2 -->|編輯| E3[編輯表單]
  E3 --> E4[儲存修改]
  E4 --> E
  E2 -->|刪除| E5[確認刪除]
  E5 --> E
  E2 -->|返回| B

  C -->|查看支出分析| F[支出分析頁面]
  F --> F1[查看分類圓餅圖 / 長條圖]
  F1 --> F2[切換月份檢視]
  F2 --> F1
  F1 --> B
```

### 流程說明

- **首頁（當月總覽）**：使用者進入網站後，首先看到當月的總收入、總支出與結餘金額，以及近期的收支紀錄摘要。
- **新增收支**：使用者可以透過表單新增一筆收入或支出。金額欄位支援直接輸入四則運算式（如 `100+50*2`），系統會自動計算結果。日期預設為今日，也可手動選擇其他日期。
- **歷史紀錄**：使用者可以瀏覽所有收支紀錄，並依月份進行篩選。每筆紀錄都可以進行編輯或刪除操作。
- **支出分析**：使用者可以查看支出的統計圖表（圓餅圖或長條圖），依分類或月份來分析消費習慣。

---

## 2. 系統序列圖（Sequence Diagram）

### 2-1. 新增一筆收支紀錄

描述使用者從填寫表單到資料寫入資料庫的完整流程。

```mermaid
sequenceDiagram
  actor User as 使用者
  participant Browser as 瀏覽器
  participant Flask as Flask Route
  participant Model as Transaction Model
  participant DB as SQLite

  User->>Browser: 點擊「新增收支」
  Browser->>Flask: GET /transactions/new
  Flask-->>Browser: 回傳新增表單頁面 (form.html)

  User->>Browser: 填寫金額 (如 100+50)、分類、日期、備註
  Note over Browser: JS 即時計算金額：100+50 = 150
  User->>Browser: 點擊「送出」

  Browser->>Flask: POST /transactions
  Flask->>Flask: 驗證表單資料
  Flask->>Model: 建立 Transaction 物件
  Model->>DB: INSERT INTO transactions (type, amount, category, date, note)
  DB-->>Model: 寫入成功
  Model-->>Flask: 回傳成功
  Flask-->>Browser: 302 重導向至首頁 (/)
  Browser->>Flask: GET /
  Flask->>Model: 查詢當月收支總計
  Model->>DB: SELECT ... WHERE month = 當月
  DB-->>Model: 回傳資料
  Model-->>Flask: 回傳彙整結果
  Flask-->>Browser: 回傳首頁 (index.html)
```

### 2-2. 查看首頁（當月總覽）

描述使用者進入首頁時，系統如何從資料庫撈取並呈現當月財務摘要。

```mermaid
sequenceDiagram
  actor User as 使用者
  participant Browser as 瀏覽器
  participant Flask as Flask Route
  participant Model as Transaction Model
  participant DB as SQLite

  User->>Browser: 開啟首頁
  Browser->>Flask: GET /
  Flask->>Model: 查詢當月收入總額
  Model->>DB: SELECT SUM(amount) WHERE type='income' AND month=當月
  DB-->>Model: 回傳收入總額
  Flask->>Model: 查詢當月支出總額
  Model->>DB: SELECT SUM(amount) WHERE type='expense' AND month=當月
  DB-->>Model: 回傳支出總額
  Flask->>Model: 查詢近期收支紀錄
  Model->>DB: SELECT * ORDER BY date DESC LIMIT N
  DB-->>Model: 回傳紀錄列表
  Model-->>Flask: 彙整所有資料
  Flask-->>Browser: 回傳首頁 (index.html) 含總收入、總支出、結餘、近期紀錄
  Browser-->>User: 顯示當月總覽畫面
```

### 2-3. 查看支出分析

描述使用者查看支出統計圖表時，系統的資料查詢流程。

```mermaid
sequenceDiagram
  actor User as 使用者
  participant Browser as 瀏覽器
  participant Flask as Flask Route
  participant Model as Transaction Model
  participant DB as SQLite

  User->>Browser: 點擊「支出分析」
  Browser->>Flask: GET /analysis?month=2026-04
  Flask->>Model: 查詢指定月份各分類支出
  Model->>DB: SELECT category, SUM(amount) WHERE type='expense' GROUP BY category
  DB-->>Model: 回傳分類統計資料
  Model-->>Flask: 回傳統計結果
  Flask-->>Browser: 回傳分析頁面 (analysis.html) 含圖表資料
  Note over Browser: Chart.js 根據資料渲染圓餅圖/長條圖
  Browser-->>User: 顯示支出分析圖表
```

---

## 3. 功能清單對照表

以下表格列出所有功能對應的 URL 路徑、HTTP 方法與簡要說明。

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| 首頁（當月總覽） | `/` | GET | 顯示當月總收入、總支出、結餘及近期紀錄 |
| 新增收支表單 | `/transactions/new` | GET | 顯示新增收入/支出的表單頁面 |
| 送出新增收支 | `/transactions` | POST | 處理表單提交，將紀錄寫入資料庫 |
| 歷史紀錄列表 | `/transactions` | GET | 顯示所有收支紀錄，支援依月份篩選 |
| 編輯收支表單 | `/transactions/<id>/edit` | GET | 顯示指定紀錄的編輯表單 |
| 更新收支紀錄 | `/transactions/<id>` | POST | 處理編輯表單提交，更新資料庫中的紀錄 |
| 刪除收支紀錄 | `/transactions/<id>/delete` | POST | 刪除指定的收支紀錄 |
| 支出分析 | `/analysis` | GET | 顯示支出統計圖表（支援月份篩選） |
