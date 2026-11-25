# 【台農院】大臺北瑠公圳水系圖（網頁地圖）

開啟 `index.html` 即可使用（需連網：底圖與古地圖由各機關即時提供）。手機定位功能須以 https 網址開啟。

## 檔案
- `index.html`：網頁本體（Leaflet 1.9.4）
- `data/canals.js`：水圳線，由上層 `大台北地區水圳、溝渠.kml` 轉出（518 個圖徵，依名稱合併為 453 條目）
- `data/layers.js`：古地圖目錄 209 張（北市都發局 54、中研院臺北 84、中研院全臺 71），含實測最大縮放級
- `tools/`：重建資料用的腳本

## 重建資料
1. KML 更新後：`python3 tools/kml2js.py ../大台北地區水圳、溝渠.kml data/canals.js`
2. 古地圖目錄：先取得三個 GetCapabilities 並整理為 `urls.tsv`，跑 `tools/probe2.py` 測最大縮放級，再跑 `tools/build_layers.py`。常用圖（★）清單寫在 `build_layers.py` 的 `FEAT`。

## 圖資服務
- 臺北市都發局：使用 `https://historygis.udd.gov.taipei/WMTS/`（Web Mercator 版）。`WMTS_97/` 為 TWD97 圖磚，無法與一般網頁底圖直接套疊，且舊航照只在 Web Mercator 版提供。
- 中研院臺北百年歷史地圖：`https://gis.sinica.edu.tw/taipei/wmts`
- 中研院臺灣百年歷史地圖：`https://gis.sinica.edu.tw/tileserver/wmts`（只收錄與大臺北範圍重疊者）
- 中研院伺服器宣稱各圖最大到第 19 級，實際超過原始解析度時會回傳空白圖磚，故以 `probe2.py` 逐圖實測。
