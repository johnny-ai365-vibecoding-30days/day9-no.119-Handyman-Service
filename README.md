# day9-no.119-Handyman-Service

這個專案將高雄三民區 30 間水電相關店家的資料轉成 GitHub Pages 靜態網站。資料來源為 `從-google.com.tw-抓取細節--6--2025-12-11.csv`，並在 `docs/` 中提供首頁與每家店的獨立介紹頁。

## 主要檔案
- `generate_pages.py`：從 CSV 產生 `docs/index.html` 及 `docs/stores/*.html` 的腳本，同時建立基本樣式檔。
- `docs/`：GitHub Pages 的根目錄，包含首頁、各店家頁面與 `assets/style.css`。

## 如何重新產生頁面
1. 安裝 Python 3（系統已內建即可）。
2. 在專案根目錄執行：
   ```bash
   python generate_pages.py
   ```
   執行後會依 CSV 最新內容覆寫 `docs/` 內的頁面與樣式。

## 部署到 GitHub Pages
將此專案推送到 GitHub 後，在專案設定的 Pages（或 Pages / Source）中選擇 `docs` 資料夾作為來源，等待部屬完成即可在 GitHub Pages 上看到店家列表與各自的獨立網站。
