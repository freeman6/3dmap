import sys, json, re, xml.etree.ElementTree as ET
from collections import Counter
src, out = sys.argv[1], sys.argv[2]
ns = {'k': 'http://www.opengis.net/kml/2.2'}
root = ET.parse(src).getroot()
doc = root.find('k:Document', ns)
CAT = {'F00014': '瑠公水圳', 'F01478': '其他水圳', '0078F0': '排水溝渠', '1414F0': '自然水系'}
def coords(el):
    pts = []
    for tok in (el.text or '').split():
        p = tok.split(',')
        pts.append([round(float(p[0]), 6), round(float(p[1]), 6)])
    return pts
feats = []; fid = 0
for folder in doc.findall('k:Folder', ns):
    fname = folder.find('k:name', ns).text.strip()
    for pm in folder.findall('.//k:Placemark', ns):
        name = (pm.findtext('k:name', '', ns) or '').strip()
        desc = (pm.findtext('k:description', '', ns) or '').strip()
        su = pm.findtext('k:styleUrl', '', ns)
        m = re.match(r'#(line|poly|icon)-(?:\d+-)?([0-9A-F]{6})-(\d+)?', su)
        m2 = re.search(r'-([0-9A-F]{6})-', su)
        color = m2.group(1) if m2 else None
        wm = re.match(r'#line-[0-9A-F]{6}-(\d+)', su)
        width = int(wm.group(1)) / 1000 if wm else None
        geoms = []
        for ls in pm.iter('{http://www.opengis.net/kml/2.2}LineString'):
            geoms.append(('LineString', coords(ls.find('k:coordinates', ns))))
        for pg in pm.iter('{http://www.opengis.net/kml/2.2}Polygon'):
            geoms.append(('Polygon', [coords(pg.find('.//k:outerBoundaryIs//k:coordinates', ns))]))
        for pt in pm.iter('{http://www.opengis.net/kml/2.2}Point'):
            geoms.append(('Point', coords(pt.find('k:coordinates', ns))[0]))
        if len(geoms) != 1: print('multi/none', name, len(geoms))
        g = geoms[0]
        fid += 1
        feats.append({'type': 'Feature', 'id': fid,
            'properties': {'name': name, 'desc': desc, 'folder': fname, 'cat': CAT.get(color, color), 'color': '#' + color, 'w': width},
            'geometry': {'type': g[0], 'coordinates': g[1]}})
print(len(feats), Counter((f['properties']['cat'], f['geometry']['type']) for f in feats))
print(Counter(f['properties']['folder'] for f in feats))
loose = doc.findall('k:Placemark', ns); print('loose placemarks', len(loose))
with open(out, 'w', encoding='utf-8') as fh:
    fh.write('// 來源：大台北地區水圳、溝渠.kml（Google 我的地圖匯出）；由 kml2js.py 轉換\n')
    fh.write('window.CANALS = ' + json.dumps({'type': 'FeatureCollection', 'features': feats}, ensure_ascii=False, separators=(',', ':')) + ';\n')
