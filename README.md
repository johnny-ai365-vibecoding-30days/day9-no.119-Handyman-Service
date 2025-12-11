# Handyman Service GitHub Pages Builder

此專案會從 `從-google.com.tw-抓取細節--6--2025-12-11.csv` 讀取水電行資料，並在 `docs/` 產生可直接部署到 GitHub Pages 的靜態網站：

- `docs/index.html`：所有水電行的目錄頁，連結到各自的獨立網站。
- `docs/<slug>/index.html`：每一家店的單頁網站，含地址、評分、營業狀態、電話與 Google 地圖連結。

## 重新產生網站
1. 確認 CSV 檔案存在於專案根目錄。
2. 執行建置腳本：
   ```bash
   python build_sites.py
   ```
3. 腳本會更新 `docs/` 目錄；將變更推送後，即可透過 GitHub Pages 發佈。

若需要調整樣式，可編輯 `docs/style.css`；若要修改輸出內容或欄位對應，請更新 `build_sites.py`。
