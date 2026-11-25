import csv, math, json, sys, urllib.request, concurrent.futures as cf
rows = [r for r in csv.reader(open(sys.argv[1]), delimiter='\t')]
TP = (121.45, 24.97, 121.63, 25.13)
def tx(lon, z): return int((lon+180)/360*2**z)
def ty(lat, z): return int((1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*2**z)
def get(tpl, z, x, y):
    u = tpl.replace('{TileMatrix}', str(z)).replace('{TileRow}', str(y)).replace('{TileCol}', str(x))
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 map-probe'})
        with urllib.request.urlopen(req, timeout=25) as r: return len(r.read())
    except Exception: return -1
def exists(s): return s > 0 and s != 935
def probe(r):
    src, lid, title, tpl, bb, _ = r
    b = list(map(float, bb.split()))
    W, S, E, N = max(b[0], TP[0]), max(b[1], TP[1]), min(b[2], TP[2]), min(b[3], TP[3])
    if not (W < E and S < N): return lid, {'skip': 'outside'}
    start = None
    for z in (10, 11, 12, 13, 14):
        for x in range(tx(W, z), tx(E, z)+1):
            for y in range(ty(N, z), ty(S, z)+1):
                if exists(get(tpl, z, x, y)): start = (z, x, y); break
            if start: break
        if start: break
    if not start: return lid, {'skip': 'nodata'}
    z, x, y = start; minz = z
    while z < 20:
        nxt = None
        for dx in (0, 1):
            for dy in (0, 1):
                if exists(get(tpl, z+1, 2*x+dx, 2*y+dy)): nxt = (z+1, 2*x+dx, 2*y+dy); break
            if nxt: break
        if not nxt: break
        z, x, y = nxt
    return lid, {'start': minz, 'max': z}
todo = [r for r in rows if r[0] != 'udd' and not (r[1].startswith('TPE_') and r[1] != 'TPE_all')]
print('layers', len(todo))
out = {}
with cf.ThreadPoolExecutor(6) as ex:
    for lid, res in ex.map(probe, todo): out[lid] = res
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
from collections import Counter
print(Counter(str(v.get('max', v.get('skip'))) for v in out.values()))
