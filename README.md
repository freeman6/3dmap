# 【台農院】大臺北瑠公圳水系圖（網頁地圖）

開啟 `index.html` 即可使用（需連網：底圖與古地圖由各機關即時提供）。手機定位功能須以 https 網址開啟。

## 檔案
- `index.html`：網頁本體（Leaflet 1.9.4）
- `data/canals.js`：水圳線，由上層 `大台北地區水圳、溝渠.kml` 轉出（518 個圖徵，依名稱合併為 453 條目）
- `data/landmarks.js`：地標（名稱、地址、WGS84 座標、`tour` 巡覽順序），可直接增修
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

## 3D 巡覽
標題列「▶ 巡覽」按鈕或地圖右上角「3D」按鈕（巡覽中標題列按鈕變為「■ 結束巡覽」）：依 `landmarks.js` 的 `tour` 順序以 3D 視角飛行巡覽，每點停留 5 秒（`index.html` 的 `TOUR_STAY`）。抵達時跳出懸浮視窗：介紹文字取自 `landmarks.js` 的 `info`，「附近水圳」由地圖水圳資料即時計算（400 公尺內最近 3 條）；起飛前往下一點時關閉。視窗內有「疊加 1939瑠公水利組合區域圖」按鈕（圖層 id 由 `index.html` 的 `TOUR_OLD` 指定），開啟後整趟巡覽保留，結束巡覽時同步套疊到 2D 地圖。按下時才載入 MapLibre GL 4.7.1；地形取自 AWS Terrain Tiles（terrarium）。瀏覽器需支援 WebGL；系統設定「減少動態效果」時改為直接切換。

左側「水圳／古地圖」選單預設隱藏，開關按鈕（`#bSide`）目前也隱藏；點選地圖上的水圳或開啟帶 `c=` 的分享連結時會自動展開顯示詳細資料，關閉詳細資料即收合。要恢復按鈕，移除 `index.html` 中 `#bSide` 的 `hidden` 屬性即可。

水圳類別預設全部關閉，由使用者在左側或圖例勾選開啟；分享連結帶有 `c=` 指定水圳時，會自動開啟該水圳所屬類別。
