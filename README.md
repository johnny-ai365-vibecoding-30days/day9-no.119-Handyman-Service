# day9-no.119-Handyman-Service

以 `從-google.com.tw-抓取細節--6--2025-12-11.csv` 的 30 筆水電行資料，產生可直接部署到 GitHub Pages 的靜態網站。

## 產出內容
- `docs/index.html`：所有水電行的導覽頁，含評分、地址、營業狀態與快速撥打電話連結。
- `docs/stores/<slug>/index.html`：每間店家的獨立頁面，提供完整資訊與地圖連結。
- `docs/assets/style.css`：深色系介面與按鈕樣式。
- `docs/data/businesses.json`：已整理過的店家清單，可供後續程式化使用。

## 重新產生網站
1. 確認安裝 Python 3。
2. 如有更新 CSV，覆寫原始檔或調整路徑。
3. 執行：
   ```bash
   python generate_sites.py
   ```
4. 產出的檔案會覆寫 `docs/` 內頁面。

## 部署到 GitHub Pages
1. 將變更推送到 GitHub。
2. 在 GitHub 專案的 **Settings > Pages** 中，將 **Source** 設為所使用的分支，資料夾選擇 `docs/`。
3. 儲存設定後，即可在 Pages 網址上查看每個水電行的獨立網站。
