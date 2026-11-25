import csv, json, re, sys
caps = sys.argv[1]; out = sys.argv[2]
rows = list(csv.reader(open(caps + '/urls.tsv'), delimiter='\t'))
probe = {}
for f in ('probe2.json', 'probe4.json'):
    probe.update(json.load(open(caps + '/' + f)))
FEAT = {  # 精選：古圳調查常用，附一句用途
 'liugong_1939': '瑠公水利組合灌區與圳路，日治末期',
 'liugong_1957': '戰後瑠公灌區與給水路',
 'JM20K_1904': '日治初期地形、聚落、圳路與埤塘',
 'JM20K_1921': '堡圖大正修正版，可與 1904 年版比對',
 'JM25K_1921': '日治地形圖，等高線與水系較清楚',
 'TPE_all': '日治地籍圖，可對照地號與水路地',
 'Taipei_3K_1937': '1:3000 大比例尺，市區細部',
 'JM1M_1931': '全臺埤圳組合灌排區域（小比例尺）',
 'Taipei_aerialphoto_1944': '美軍航照，圳路尚未加蓋',
 'Image_1945B': '都發局 1945 航照（轟炸前）',
 'Image_1947': '都發局 1947 航照',
 'Image_1956': '都發局 1956 航照，都市擴張前',
 'History_TM47': '都發局 1958 年版地形圖',
 'Taipei_1.2K_1958': '1:1200 地形圖，可見溝渠位置',
 'Image_1963': '都發局 1963 航照',
 'TM25K_1966': '戰後二萬五千分一地形圖',
 'TM50K_1966': '水利工程、水文站位置',
 'Image_1972': '都發局 1972 航照，圳路陸續加蓋期',
 '1979_Landuse_25K_Taipei': '土地灌溉利用，灌區範圍',
}
SRC = {'udd': '北市都發局', 'tp': '中研院・臺北', 'tw': '中研院・全臺'}
def year(title, lid, src):
    m = re.search(r'(1[6-9]\d\d|20[0-2]\d)', title)
    if m: return int(m.group(1)), True
    m = re.match(r'(\d{2,3})年', title)
    if m and src == 'udd': return int(m.group(1)) + 1911, True
    m = re.search(r'(1[6-9]\d\d|20[0-2]\d)', lid)
    if m: return int(m.group(1)), False
    return None, False
L = []
for src, lid, title, tpl, bb, _ in rows:
    if src == 'udd' and lid in ('EMap', 'EMap_nolabel'): continue
    if src != 'udd':
        if lid.startswith('TPE_') and lid != 'TPE_all': continue
        p = probe.get(lid)
        if not p or 'skip' in p: continue
        mx, mn = p['max'], p['start']
    else:
        mx, mn = 19, 0
    b = list(map(float, bb.split()))
    b = [round(min(b[1], b[3]), 5), round(min(b[0], b[2]), 5), round(max(b[1], b[3]), 5), round(max(b[0], b[2]), 5)]  # s,w,n,e
    url = (tpl.replace('{Style}', 'default').replace('{TileMatrixSet}', 'GoogleMapsCompatible')
              .replace('{TileMatrix}', '{z}').replace('{TileRow}', '{y}').replace('{TileCol}', '{x}'))
    y, sure = year(title, lid, src)
    t = title.strip()
    if src == 'udd' and y: t = re.sub(r'^\d{2,3}年', f'{y}（民國{y-1911}年）', t)
    d = {'id': lid, 't': t, 's': src, 'u': url, 'b': b, 'mx': mx}
    if mn: d['mn'] = mn
    if y: d['y'] = y
    if y and not sure: d['yq'] = 1
    if lid in FEAT: d['f'] = FEAT[lid]
    L.append(d)
L.sort(key=lambda d: (d.get('y', 9999), d['s'], d['t']))
miss = set(FEAT) - {d['id'] for d in L}
print(len(L), 'layers;', {k: sum(1 for d in L if d['s'] == k) for k in SRC}, 'featured', sum(1 for d in L if 'f' in d), 'missing', miss)
with open(out, 'w', encoding='utf-8') as fh:
    fh.write('// 古地圖圖層目錄：由各 WMTS GetCapabilities 產生（2026-11-26）；mx＝實測最大原生縮放級\n')
    fh.write('window.SOURCES = ' + json.dumps(SRC, ensure_ascii=False) + ';\n')
    fh.write('window.OLDMAPS = ' + json.dumps(L, ensure_ascii=False, separators=(',', ':')).replace('},{', '},\n{') + ';\n')
