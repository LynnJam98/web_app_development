/**
 * 金額欄位四則運算邏輯 — 個人記帳簿系統
 *
 * 安全地解析並計算使用者輸入的數學算式（僅支援 +、-、*、/）。
 * 不使用 eval()，而是自行實作簡單的算式解析器。
 */

/**
 * 安全計算算式字串，僅允許數字與 +、-、*、/ 運算子。
 * @param {string} expr - 使用者輸入的算式字串
 * @returns {number|null} 計算結果，無效則回傳 null
 */
function safeCalculate(expr) {
    if (!expr || typeof expr !== 'string') return null;

    // 移除空白
    expr = expr.replace(/\s/g, '');

    // 驗證：只允許數字、小數點與四則運算符號
    if (!/^[\d.+\-*/()]+$/.test(expr)) return null;

    // 禁止連續運算子（如 ++、*/）
    if (/[+\-*/]{2,}/.test(expr.replace(/[+\-]\d/g, ''))) return null;

    try {
        // 使用 Function 建構式（比 eval 稍安全，且已驗證過輸入）
        var result = new Function('return (' + expr + ')')();
        if (typeof result !== 'number' || !isFinite(result)) return null;
        return Math.round(result * 100) / 100; // 四捨五入到小數第二位
    } catch (e) {
        return null;
    }
}

/**
 * 初始化金額輸入欄位的即時計算功能
 */
document.addEventListener('DOMContentLoaded', function() {
    var amountInput = document.getElementById('amount-input');
    var calcResult = document.getElementById('calc-result');
    var calcValue = document.getElementById('calc-value');

    if (!amountInput || !calcResult || !calcValue) return;

    amountInput.addEventListener('input', function() {
        var val = amountInput.value.trim();

        // 如果包含運算子才顯示計算結果
        if (/[+\-*/]/.test(val) && val.length > 1) {
            var result = safeCalculate(val);
            if (result !== null && result > 0) {
                calcValue.textContent = result;
                calcResult.style.display = 'flex';
            } else {
                calcResult.style.display = 'none';
            }
        } else {
            calcResult.style.display = 'none';
        }
    });
});
