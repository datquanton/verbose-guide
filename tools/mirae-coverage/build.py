#!/usr/bin/env python3
"""Build the Mirae Asset coverage pages (milestones, drivers, cushion) into /nganh/.

Inputs (this folder):  data.json   per-ticker reading of Mirae Asset Vietnam reports (see README.md)
                       market.json prices and trailing multiples from FiinQuantX
                       meta.json   hand-written titles, key points and tiles for each page
Run:  python3 tools/mirae-coverage/build.py      (from the repository root)
      Also (re)places the overview card on / and /en/, then runs tools/industry-index/build.py; re-running is safe. --no-index skips both.
"""
import json, os, re, html, statistics, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))
MK = json.load(open(os.path.join(HERE, 'market.json'), encoding='utf-8'))
META = json.load(open(os.path.join(HERE, 'meta.json'), encoding='utf-8'))
WHENS = json.load(open(os.path.join(HERE, 'whens.json'), encoding='utf-8'))
SC = json.load(open(os.path.join(HERE, 'scorecard.json'), encoding='utf-8'))      # chart figures: 9M progress, balance sheet, bank coverage   # milestone label -> [Vietnamese label, calendar bucket]
PUB = META['published']            # YYYY-MM-DD
PRICE_DATE, VAL_DATE = MK['price_date'], MK['val_date']
STALE_DAYS = 100                   # a target price older than this is shown as stale

E = lambda s: html.escape(str(s), quote=True)
MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def d2(s): return datetime.date.fromisoformat(s)
def fdate(s, L):
    d = d2(s)
    return f'{d.day:02d}/{d.month:02d}/{d.year}' if L == 'vi' else f'{d.day} {MON[d.month-1]} {d.year}'
def num(x, L, dec=0):
    s = f'{x:,.{dec}f}'
    return s.replace(',', '§').replace('.', ',').replace('§', '.') if L == 'vi' else s
def pct(x, L, dec=0, sign=True):
    s = num(abs(x), L, dec) + '%'
    if x < 0: return '−' + s
    return ('+' + s) if sign else s
def mult(x, L): return num(x, L, 1) + 'x'
def T(o, L): return o[L]

RATING_VI = {'Buy': 'Mua', 'Trading Buy': 'Tăng tỷ trọng', 'Hold': 'Nắm giữ', 'Sell': 'Bán'}
def rating_txt(r, L):
    if not r: return 'chưa xếp hạng' if L == 'vi' else 'not rated'
    return RATING_VI.get(r, r) if L == 'vi' else r
def pick(r, L):
    cls = 'buy' if r in ('Buy', 'Trading Buy') else 'hold'
    return f'<span class="pick {cls}">{E(rating_txt(r, L))}</span>'

# ---------- "when" labels: sort key and Vietnamese form ----------
VI_MON = {m: i + 1 for i, m in enumerate(MON)}
def when_key(w):
    """Sortable (year, position-in-year) for a milestone label; passed milestones sort first."""
    s = w.lower()
    passed = s.startswith('passed')
    m = re.search(r'([1-4])q(\d\d)', s)
    y = None; pos = 0.5
    if m: y = 2000 + int(m.group(2)); pos = (int(m.group(1)) - 0.5) / 4
    else:
        m = re.search(r'([12])h(\d\d)', s)
        if m: y = 2000 + int(m.group(2)); pos = 0.26 if m.group(1) == '1' else 0.76
        else:
            m = re.search(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.? (20\d\d)', s)
            if m: y = int(m.group(2)); pos = (VI_MON[m.group(1).capitalize()] - 0.5) / 12
            else:
                m = re.search(r'(?:fy)?(20\d\d|\d\d)(?!\d)', s)
                if m:
                    y = int(m.group(1)); y = y + 2000 if y < 100 else y
                    pos = 0.05 if 'early' in s else 0.95 if ('end' in s or 'late' in s or 'fy' in s) else 0.5 if 'mid' in s else 0.55
    if y is None: y = 2099
    return (0 if passed else 1, y + pos)
BUCKET_ORDER = {'passed': 0, '4Q26': 1, 'fy26': 2, '1Q27': 3, '2Q27': 4, '2H27': 5, 'later': 6, 'pending': 7}
def bucket(w):
    """Calendar bucket for the overview page (hand-checked map first, pattern rules as fallback)."""
    if w in WHENS: return WHENS[w][1]
    p, k = when_key(w)
    if p == 0: return 'passed'
    if k < 2027: return '4Q26'
    if k < 2027.25: return '1Q27'
    if k < 2027.5: return '2Q27'
    if k < 2028: return '2H27'
    return 'later'
def when_vi(w):
    s = w
    s = re.sub(r'^passed:?\s*', 'đã qua: ', s, flags=re.I)
    s = re.sub(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? (20\d\d)', lambda m: f'{VI_MON[m.group(1)]}/{m.group(2)}', s)
    for a, b in [(r'\bearly[- ]', 'đầu '), (r'\bmid[- ]', 'giữa '), (r'\b(end|late)[- ](of[- ])?', 'cuối '), (r'\bfrom\b', 'từ'), (r'\bby\b', 'trước'),
                 (r'\bonwards?\b', 'trở đi'), (r'\bongoing\b', 'đang diễn ra'), (r'\bquarterly\b', 'hằng quý'), (r'\beach quarter\b', 'mỗi quý'),
                 (r'\band\b', 'và'), (r'\bto\b', 'đến'), (r'\bAGM\b', 'ĐHĐCĐ'), (r'\bresults\b', 'KQKD'), (r'\bannual\b', 'hằng năm'),
                 (r'\bFY(\d\d)F?\b', r'năm 20\1'), (r'\bseason\b', 'mùa'), (r'\bthrough\b', 'đến hết'), (r'\buntil\b', 'đến'),
                 (r'\bcrop\b', 'vụ'), (r'\bafter\b', 'sau'), (r'\bbefore\b', 'trước'), (r'\bevery\b', 'mỗi'), (r'\bmonthly\b', 'hằng tháng'),
                 (r'\bexpected\b', 'dự kiến'), (r'\btarget\b', 'mục tiêu'), (r'\bno date\b', 'chưa có ngày'), (r'\bundated\b', 'chưa có ngày')]:
        s = re.sub(a, b, s, flags=re.I)
    return s
def when_lbl(w, L): return (WHENS[w][0] if w in WHENS else when_vi(w)) if L == 'vi' else w
def ms_sort(w): return (BUCKET_ORDER[bucket(w)], when_key(w))

# ---------- derived numbers ----------
TK = {t['ticker']: t for t in D['tickers']}
for t in D['tickers']:
    m = MK['data'][t['ticker']]
    t['px'], t['pe'], t['pb'] = m['price'], m['pe'], m['pb']
    t['gap'] = (t['tp'] / t['px'] - 1) * 100 if t.get('tp') else None
    t['absorb'] = (1 - t['px'] / t['tp']) * 100 if t.get('tp') and t['tp'] > t['px'] else (0 if t.get('tp') else None)
    t['since'] = (t['px'] / t['price_at_tp_date'] - 1) * 100 if t.get('tp') and t.get('price_at_tp_date') else None
    t['age'] = (d2(PUB) - d2(t['tp_date'])).days if t.get('tp_date') and t.get('tp') else None
    t['stale'] = bool(t.get('tp')) and t['age'] > STALE_DAYS
    t['review'] = bool(t.get('tp')) and bool(t.get('review_down')) and not t['stale']
    t['flag'] = '*' if t['stale'] else '†' if t['review'] else ''
    t['gap_then'] = (t['tp'] / t['price_at_tp_date'] - 1) * 100 if t.get('tp') and t.get('price_at_tp_date') else None
    t['fresh'] = bool(t.get('tp')) and not t['flag']
    t['prog'] = SC['progress'].get(t['ticker'])
    t['bsi'] = SC['bs'].get(t['ticker'])
    t['cov'] = SC['cov'].get(t['ticker'])

TXT = {
 'vi': dict(site='Nghiên cứu cổ phiếu Việt Nam', nav=[('vi-mo/', 'Vĩ mô'), ('nganh/', 'Ngành'), ('ket-qua-kinh-doanh/', 'Kết quả kinh doanh'), ('cfa/', 'CFA')],
   other='English', theme='Đổi giao diện sáng/tối', pub='Công bố', kick='Báo cáo ngành', keypoints='Điểm chính',
   foot='Nghiên cứu cá nhân, không phải khuyến nghị đầu tư. Quan điểm là của riêng tác giả và có thể thay đổi mà không cần báo trước.',
   drivers='Động lực cốt lõi', milestones='Mốc theo dõi', cushion='Bộ đệm', breaks='Điều gì phá vỡ luận điểm', sources='Báo cáo đã đọc',
   target='Giá mục tiêu', price='giá', gap='khoảng cách đến giá mục tiêu', none_tp='Mirae Asset không nêu giá mục tiêu trong các báo cáo gần nhất',
   th=['Mã', 'Khuyến nghị', 'Giá mục tiêu', 'Ngày báo cáo', 'Giá khi đó', 'Giá hiện tại', 'Từ ngày báo cáo', 'Đến giá mục tiêu', 'Biên an toàn', 'P/E', 'P/B'],
   ind='Ngành', when='Khi nào', what='Điều cần thấy', stale='giá mục tiêu đặt hơn 100 ngày trước', review='Mirae Asset đã báo sẽ hạ dự báo hoặc định giá', nodata='–',
   bucket={'passed': 'Vừa qua', '4Q26': 'Từ nay đến hết 2026: sự kiện có thời điểm', 'fy26': 'Kiểm chứng cả năm 2026', '1Q27': 'Đầu 2027 (1Q27, 1H27)', '2Q27': 'Quý 2/2027', '2H27': 'Phần còn lại của 2027', 'later': 'Từ 2028 trở đi', 'pending': 'Chưa có ngày hoặc chờ xác nhận'}),
 'en': dict(site='Vietnam Equity Research', nav=[('en/#vi-mo', 'Macro'), ('en/#nganh', 'Sectors'), ('en/#ket-qua-kinh-doanh', 'Earnings'), ('en/#cfa', 'CFA')],
   other='Tiếng Việt', theme='Switch light/dark theme', pub='Published', kick='Sector report', keypoints='Key points',
   foot="Personal research, not investment advice. Views are the author's own and may change without notice.",
   drivers='Underlying drivers', milestones='Milestones', cushion='Cushion', breaks='What breaks the thesis', sources='Reports read',
   target='Target price', price='price', gap='gap to target', none_tp='Mirae Asset states no target price in its latest notes',
   th=['Ticker', 'Rating', 'Target', 'Report date', 'Price then', 'Price now', 'Since report', 'Gap to target', 'Margin of safety', 'P/E', 'P/B'],
   ind='Industry', when='When', what='What to see', stale='target set more than 100 days ago', review='Mirae Asset has said it will likely cut forecasts or valuation', nodata='–',
   bucket={'passed': 'Just passed', '4Q26': 'From now to end-2026: dated events', 'fy26': 'Full-year 2026 checks', '1Q27': 'Early 2027 (1Q27, 1H27)', '2Q27': '2Q27', '2H27': 'Rest of 2027', 'later': '2028 onwards', 'pending': 'Undated or awaiting confirmation'}),
}

CSS = """
.tk h3{font-size:20px;margin:18px 0 2px;display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 10px}
.tk h3 .sym{font-variant-numeric:tabular-nums;color:var(--series-1)}
.tk h3 .nm{font-weight:600}
.tkline{font-size:13.5px;color:var(--text-muted);margin:0 0 8px;max-width:none;font-variant-numeric:tabular-nums}
.thesis{margin:6px 0 10px}
.tri{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:12px 0}
@media (max-width:860px){.tri{grid-template-columns:1fr}}
.tri>div{background:var(--surface-1);border:1px solid var(--border);border-radius:10px;padding:12px 16px 8px}
.tri h4{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--text-muted);margin:0 0 4px}
.tri ul{padding-left:18px;margin:4px 0}.tri li{font-size:14.5px;line-height:1.5;margin:7px 0;max-width:none}
.when{display:inline-block;font-size:11.5px;font-weight:700;color:var(--series-1);border:1px solid var(--border);border-radius:999px;padding:0 7px;margin-right:4px;font-variant-numeric:tabular-nums}
.when.past{color:var(--text-muted)}
.brk{font-size:14.5px;border-left:3px solid var(--critical);padding:2px 0 2px 12px;margin:10px 0;color:var(--text-secondary)}
.note2{font-size:13px;color:var(--text-muted);margin:6px 0}
.src{font-size:12.5px;color:var(--text-muted);margin:8px 0 0;max-width:none}
.tablewrap th{cursor:pointer;user-select:none;white-space:nowrap}.tablewrap th[aria-sort=ascending]::after{content:" ▲"}.tablewrap th[aria-sort=descending]::after{content:" ▼"}
.tablewrap td.t{font-size:14px;max-width:none}.tablewrap td a{font-weight:600}
.old{color:var(--text-muted)}
.jump{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}.jump a{font-size:13px;font-weight:600;border:1px solid var(--border);border-radius:999px;padding:1px 10px;background:var(--surface-1);font-variant-numeric:tabular-nums}
.cal h3{margin-top:26px}.cal ul{padding-left:18px}.cal li{font-size:15px;max-width:80ch}
.cal .sym{font-weight:700;margin-right:4px}
details.more{margin:10px 0}details.more summary{cursor:pointer;font-size:16px;font-weight:650;margin:18px 0 4px}
.barrow .bar.neg{background:var(--critical)}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr));gap:0 20px}.grid2 figure.viz{margin:20px 0}
.legend{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12.5px;color:var(--text-secondary);margin:-6px 0 12px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
.legend i.k0,.legend i.k1{border-radius:50%;width:10px;height:10px}.legend i.k0{border:2px solid var(--series-1);background:var(--surface-1)}
.legend i.k1{background:var(--series-1)}.legend i.k1.m{background:var(--text-muted)}.legend i.pk{width:2px;height:12px;border-radius:0;background:var(--text-primary);opacity:.55}
.db{display:grid;grid-template-columns:var(--dbn,92px) 1fr 116px;align-items:center;gap:10px;padding:4px 0;border-radius:6px}
.db:hover,.db:focus{background:color-mix(in srgb,var(--series-1) 8%,transparent);outline:none}
.db .name{font-size:13px;color:var(--text-secondary);text-align:right;line-height:1.25}
.db .trk{position:relative;height:18px}.db .trk i{position:absolute;display:block}
.db .zero{top:-4px;bottom:-4px;width:1px;background:var(--baseline)}
.db .ln{top:8px;height:2px;background:var(--series-1-soft)}
.db .d0,.db .d1{top:3px;width:12px;height:12px;margin-left:-6px;border-radius:50%}
.db .d0{background:var(--surface-1);border:2px solid var(--series-1)}
.db .d1{background:var(--series-1);box-shadow:0 0 0 2px var(--surface-1)}
.db.mut .d0{border-color:var(--text-muted)}.db.mut .d1{background:var(--text-muted)}.db.mut .ln{background:var(--grid)}
.db .val{font-size:12.5px;color:var(--text-secondary);font-variant-numeric:tabular-nums;white-space:nowrap}.db .val b{color:var(--text-primary)}
.db.ax{padding:0}.db.ax .trk{height:16px}.db.ax .trk i{font-style:normal;font-size:11px;color:var(--text-muted);transform:translateX(-50%);top:0;font-variant-numeric:tabular-nums}
@media (max-width:560px){.db{grid-template-columns:var(--dbm,62px) 1fr 96px;gap:6px}.db .val{font-size:11.5px}}
figure.viz.ind{--dbn:170px;--dbm:96px}
.barrow.pg:focus{outline:none;background:color-mix(in srgb,var(--series-1) 8%,transparent)}
.barrow .track .pace{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--text-primary);opacity:.45;z-index:1}
.tablewrap td .sub{display:block;font-size:11.5px;color:var(--text-muted);font-weight:400;white-space:normal;max-width:24ch}
.tablewrap td.num .sub{margin-left:auto}
table.sc td.t{min-width:13ch}table.sum td.t{min-width:24ch;white-space:normal}table.sum td.lst{min-width:16ch;font-size:13px}table.sum td.lst b{color:var(--text-primary)}
figure.viz.solo{max-width:760px}
table.sum th,table.sc th{white-space:normal;min-width:9ch}
details.tk{border-top:1px solid var(--grid);margin-top:8px;padding:2px 0 6px}
details.tk>summary{cursor:pointer;list-style:none}details.tk>summary::-webkit-details-marker{display:none}
details.tk>summary h3::after{content:"+";margin-left:auto;font-weight:400;color:var(--text-muted)}details.tk[open]>summary h3::after{content:"−"}
details.tk>summary .thesis{color:var(--text-secondary);font-size:15px;margin:4px 0 8px}
.tog{margin:6px 0 4px}.tog button{background:var(--surface-1);color:var(--text-secondary);border:1px solid var(--border);border-radius:8px;padding:3px 10px;margin-right:8px;font:inherit;font-size:13px;cursor:pointer}
.crumb a{color:inherit}.crumb a:hover{color:var(--series-1);text-decoration:none}
details.howto{margin:18px 0 0;font-size:14.5px;color:var(--text-secondary);max-width:80ch}details.howto summary{cursor:pointer;color:var(--series-1);font-weight:600}details.howto p{margin:8px 0 0}
#tip{position:fixed;pointer-events:none;background:var(--text-primary);color:var(--page);font-size:12.5px;padding:5px 8px;border-radius:6px;max-width:300px;opacity:0;transition:opacity .08s;z-index:9}
.pick{white-space:nowrap}
"""
SORT_JS = """<script>document.querySelectorAll('table.sort').forEach(function(tb){var ths=tb.querySelectorAll('th');ths.forEach(function(th,i){th.addEventListener('click',function(){
var body=tb.tBodies[0],rows=[].slice.call(body.rows),dir=th.getAttribute('aria-sort')==='descending'?1:-1;ths.forEach(function(h){h.removeAttribute('aria-sort')});
th.setAttribute('aria-sort',dir<0?'descending':'ascending');rows.sort(function(a,b){var x=a.cells[i].dataset.v,y=b.cells[i].dataset.v;
if(x===undefined){return dir*a.cells[i].textContent.localeCompare(b.cells[i].textContent)}x=x===''?-1e18:+x;y=y===''?-1e18:+y;return dir*(x-y)});
rows.forEach(function(r){body.appendChild(r)})})})});</script>"""
JS_ADD = '<div id="tip" role="tooltip"></div><script>(function(){var t=document.getElementById(\'tip\');\nfunction show(el,x,y){t.textContent=el.getAttribute(\'data-tip\');t.style.opacity=1;var px=x+14,py=y+14;if(px+t.offsetWidth>innerWidth-8)px=x-t.offsetWidth-14;t.style.left=px+\'px\';t.style.top=py+\'px\'}\ndocument.addEventListener(\'mousemove\',function(e){var el=e.target.closest&&e.target.closest(\'[data-tip]\');if(!el){t.style.opacity=0;return}show(el,e.clientX,e.clientY)});\ndocument.addEventListener(\'focusin\',function(e){var el=e.target.closest&&e.target.closest(\'[data-tip]\');if(!el){t.style.opacity=0;return}var r=el.getBoundingClientRect();show(el,r.left+r.width/2,r.top)});\ndocument.addEventListener(\'focusout\',function(){t.style.opacity=0});\nfunction openHash(){var id=decodeURIComponent(location.hash.slice(1));var el=id&&document.getElementById(id);if(el&&el.tagName===\'DETAILS\'){el.open=true;el.scrollIntoView()}}\naddEventListener(\'hashchange\',openHash);openHash();\ndocument.querySelectorAll(\'.tog button\').forEach(function(b){b.addEventListener(\'click\',function(){var o=b.getAttribute(\'data-all\')===\'1\';document.querySelectorAll(\'details.tk\').forEach(function(d){d.open=o})})});\n})();</script>'
THEME_SVG = '<svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true" style="vertical-align:-2px"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.5a6.5 6.5 0 0 1 0 13z" fill="currentColor"/></svg>'

def shell(L, slug, title, desc, body):
    X = TXT[L]
    up = '../../' if L == 'vi' else '../../../'
    brand = up if L == 'vi' else up + 'en/'
    nav = ''.join(f'<a href="{up}{h}"' + (' aria-current="page"' if 'nganh' in h else '') + f'>{E(n)}</a>' for h, n in X['nav'])
    other = 'en/' if L == 'vi' else '../'
    return (f'<!doctype html>\n<html lang="{L}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{E(title)} · {E(X["site"])}</title><meta name="description" content="{E(desc)}">\n'
            f'<link rel="stylesheet" href="{up}assets/site.css"><script>try{{var t=localStorage.getItem(\'theme\');if(t)document.documentElement.setAttribute(\'data-theme\',t)}}catch(e){{}}</script>'
            f'<script src="{up}assets/site.js" defer></script><style>{CSS}</style></head>\n'
            f'<body><header class="topbar"><div class="inner"><a class="brand" href="{brand}">{E(X["site"])}</a><nav>{nav}</nav><span class="right">'
            f'<a href="{other}" hreflang="{"en" if L == "vi" else "vi"}">{E(X["other"])}</a><button class="theme" type="button" aria-label="{E(X["theme"])}" title="{E(X["theme"])}">{THEME_SVG}</button></span></div></header>\n'
            f'<main class="wrap">\n{body}\n{SORT_JS}\n' + JS_ADD + '\n</main>\n'
            f'<footer class="foot"><div class="inner"><p><a href="{brand}">{E(X["site"])}</a> · {E(X["foot"])}</p></div></footer>\n</body></html>\n')

def rich(s):
    """Escape, then allow **bold** in hand-written meta text."""
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', E(s))

def tiles(items, L):
    return '<div class="tiles">' + ''.join(
        f'<div class="tile"><div class="label">{E(T(i["label"], L))}</div><div class="value">{E(T(i["value"], L))}</div><div class="note">{rich(T(i["note"], L))}</div></div>'
        for i in items) + '</div>'

def cls(x): return 'up' if x > 0 else 'down' if x < 0 else ''
def gap_cell(t, L):
    if t['gap'] is None: return '<td class="num" data-v="">–</td>'
    c = 'old' if t['flag'] else cls(t['gap'])
    return f'<td class="num" data-v="{t["gap"]:.1f}"><span class="{c}">{pct(t["gap"], L)}</span>{t["flag"]}</td>'

def ms_li(m, L, sym=None):
    past = bucket(m['when']) == 'passed'
    s = f'<span class="sym">{sym}</span>' if sym else ''
    return f'<li>{s}<span class="when{" past" if past else ""}">{E(when_lbl(m["when"], L))}</span> {E(T(m, L))}</li>'

def segment_block(seg, L, n, single=False):
    X = TXT[L]
    out = ('' if single else f'<h3>{E(T(seg["name"], L))}</h3>') + f'<p>{E(T(seg["view"], L))}</p>'
    out += '<ul>' + ''.join(f'<li>{E(T(d, L))}</li>' for d in seg['drivers']) + '</ul>'
    rows = ''.join(f'<tr><td><span class="when">{E(when_lbl(m["when"], L))}</span></td><td class="t">{E(T(m, L))}</td></tr>' for m in sorted(seg['milestones'], key=lambda m: ms_sort(m['when'])))
    out += f'<div class="tablewrap"><table><thead><tr><th>{X["when"]}</th><th>{X["what"]}</th></tr></thead><tbody>{rows}</tbody></table></div>'
    return out

def how_to_read(L):
    if L == 'vi':
        return ('<details class="howto"><summary>Cách đọc: động lực cốt lõi, mốc theo dõi, bộ đệm</summary><p><strong>Động lực cốt lõi</strong> là vài biến số quyết định lợi nhuận của doanh nghiệp (sản lượng, giá bán, biên, chi phí vốn). '
                '<strong>Mốc theo dõi</strong> là sự kiện có ngày, kiểm chứng được, cho biết luận điểm còn đúng hướng hay không. <strong>Bộ đệm</strong> là thứ giới hạn mức giảm nếu động lực gây thất vọng: '
                'định giá, bảng cân đối, phần lợi nhuận đã chắc và cổ tức. Khoảng cách đến giá mục tiêu chỉ là một phần của bộ đệm, và chỉ có nghĩa khi mục tiêu còn mới.</p></details>')
    return ('<details class="howto"><summary>How to read: drivers, milestones, cushion</summary><p><strong>Underlying drivers</strong> are the few variables that set a company\'s earnings (volume, price, margin, funding cost). '
            '<strong>Milestones</strong> are dated, checkable events that show whether the thesis is still on track. <strong>Cushion</strong> is what limits the fall if the drivers disappoint: '
            'valuation, balance sheet, earnings already secured and dividends. The gap to target price is only one part of the cushion, and it means something only while the target is fresh.</p></details>')

def disclaimer(L, n_reports):
    if L == 'vi':
        return (f'<div class="disclaimer"><strong>Nguồn và giới hạn.</strong> Trang này tóm tắt nghiên cứu của Công ty Chứng khoán Mirae Asset (Việt Nam), đăng tại '
                f'<a href="https://www.masvn.com/en/cate/sector-firm-56">masvn.com, mục Ngành &amp; Doanh nghiệp</a>; khuyến nghị, giá mục tiêu và dự báo thuộc về Mirae Asset và đúng tại ngày báo cáo, không phải ngày đăng trang này. '
                f'Phần đọc theo ba khung (động lực, mốc theo dõi, bộ đệm), cột "dự báo có thể hụt" và các so sánh với giá hiện tại là của tác giả trang. Giá và hệ số định giá: FiinQuantX. '
                f'Nội dung chỉ nhằm cung cấp thông tin, không phải khuyến nghị đầu tư. Số liệu tính đến {fdate(PUB, L)}.</div>')
    return (f'<div class="disclaimer"><strong>Source and limits.</strong> This page summarises research by Mirae Asset Securities (Vietnam), published at '
            f'<a href="https://www.masvn.com/en/cate/sector-firm-56">masvn.com, Sector &amp; Firm</a>; ratings, target prices and forecasts are Mirae Asset\'s and are correct as of each report date, not the date of this page. '
            f'The reading into three frames (drivers, milestones, cushion), the "forecast miss absorbed" column and the comparisons with current prices are this site\'s own. Prices and multiples: FiinQuantX. '
            f'For information only, not investment advice. Data as of {fdate(PUB, L)}.</div>')

def keypoints(P, L):
    kp = P['points'][L]
    return f'<section class="points"><h2>{TXT[L]["keypoints"]}</h2><ul>' + ''.join(f'<li>{rich(x)}</li>' for x in kp) + '</ul></section>'

def byline(P, ts, L, n_reports):
    dates = sorted(s['date'] for t in ts for s in t['sources'])
    if L == 'vi':
        return (f'<p class="byline">Công bố {fdate(PUB, L)} · Phạm vi: {len(ts)} cổ phiếu Mirae Asset theo dõi · Số liệu: {n_reports} báo cáo Mirae Asset ({fdate(dates[0], L)} đến {fdate(dates[-1], L)}); '
                f'giá phiên sáng {fdate(PRICE_DATE, L)} · Nguồn: Mirae Asset Securities (Việt Nam), FiinQuantX</p>')
    return (f'<p class="byline">Published {fdate(PUB, L)} · Coverage: {len(ts)} tickers under Mirae Asset coverage · Data: {n_reports} Mirae Asset reports ({fdate(dates[0], L)} to {fdate(dates[-1], L)}); '
            f'prices from the morning session of {fdate(PRICE_DATE, L)} · Source: Mirae Asset Securities (Vietnam), FiinQuantX</p>')

SEC = json.load(open(os.path.join(ROOT, 'tools', 'industry-index', 'sections.json'), encoding='utf-8'))
SEC_IND = {i['id']: i for i in SEC['industries']}
def crumb(slug, L):
    r = next((r for r in SEC['reports'] if r['path'] == f'nganh/{slug}/'), None)
    idx = '../' if L == 'vi' else '../../en/'   # page nganh/<slug>/ -> nganh/ ; page nganh/<slug>/en/ -> nganh/en/
    root = ('Ngành' if L == 'vi' else 'Sectors')
    parts = [f'<a href="{idx}">{root}</a>']
    if r:
        parts += [f'<a href="{idx}#{i}">{E(SEC_IND[i][L]["name"])}</a>' for i in r['industries']]
    return '<p class="kicker crumb">' + ' › '.join(parts) + '</p>'

def write(slug, L, htmltext):
    p = os.path.join(ROOT, 'nganh', slug, '' if L == 'vi' else 'en')
    os.makedirs(p, exist_ok=True)
    open(os.path.join(p, 'index.html'), 'w', encoding='utf-8').write(htmltext)

# ---------- charts (plain HTML; one hue, emphasis for flagged rows; every value also printed or in the table) ----------
BS_TXT = {'vi': {'cash': 'Tiền mặt ròng', 'mid': 'Vừa phải', 'thin': 'Mỏng', 'na': 'Chưa nêu', 'cov_hi': 'Bao phủ ≥100%', 'cov_mid': 'Bao phủ 70-100%', 'cov_lo': 'Bao phủ <70%'},
          'en': {'cash': 'Net cash', 'mid': 'Moderate', 'thin': 'Thin', 'na': 'Not stated', 'cov_hi': 'Coverage ≥100%', 'cov_mid': 'Coverage 70-100%', 'cov_lo': 'Coverage <70%'}}
BS_RANK = {'cash': 4, 'cov_hi': 4, 'mid': 3, 'cov_mid': 3, 'thin': 1, 'cov_lo': 1, 'na': 0}
def bs_key(t):
    if t.get('cov'):
        c = t['cov']['pct']; return 'cov_hi' if c >= 100 else 'cov_mid' if c >= 70 else 'cov_lo'
    return t['bsi']['cls'] if t.get('bsi') else 'na'
def bs_detail(t, L):
    if t.get('cov'): return (f'{num(t["cov"]["pct"], L, 1)}% ({t["cov"]["when"]})')
    return T(t['bsi'], L) if t.get('bsi') else ''
def bs_cell(t, L):
    k = bs_key(t); good = BS_RANK[k] >= 4; bad = BS_RANK[k] == 1
    mark = '●' if good else '○' if bad else '◐' if BS_RANK[k] == 3 else '·'
    c = 'up' if good else 'down' if bad else ''
    return (f'<td data-v="{BS_RANK[k]}" class="t"><span class="{c}">{mark} {E(BS_TXT[L][k])}</span>'
            f'<span class="sub">{E(bs_detail(t, L))}</span></td>')

def scale_max(v, step=20, floor=40):
    return max(floor, (int(max(v) / step) + 1) * step)

def chart_fig(title, sub, legend, body, axis, cap, aria, cls=''):
    lg = f'<div class="legend">{legend}</div>' if legend else ''
    return (f'<figure class="viz{(" " + cls) if cls else ""}"><p class="viz-title">{E(title)}</p><p class="viz-sub">{E(sub)}</p>{lg}'
            f'<div role="img" aria-label="{E(aria)}">{body}</div><div class="axis-note">{axis}</div><figcaption>{cap}</figcaption></figure>')

def dumbbell(rows, L, title, sub, cap_extra='', cls=''):
    """rows: [(label, then, now, muted, tip)]. One hue: open dot = at report date, filled dot = now; flagged rows in grey."""
    if not rows: return ''
    lo = min(-10, min(min(r[1], r[2]) for r in rows)); lo = -10 * (int(-lo / 10) + (1 if -lo % 10 else 0))
    hi = scale_max([max(r[1], r[2]) for r in rows])
    x = lambda v: (v - lo) / (hi - lo) * 100
    out = ''
    for lab, a, b2, muted, tip in rows:
        l, r = sorted((x(a), x(b2)))
        out += (f'<div class="db{" mut" if muted else ""}" tabindex="0" data-tip="{E(tip)}"><span class="name">{lab}</span><span class="trk">'
                f'<i class="zero" style="left:{x(0):.1f}%"></i><i class="ln" style="left:{l:.1f}%;width:{r - l:.1f}%"></i>'
                f'<i class="d0" style="left:{x(a):.1f}%"></i><i class="d1" style="left:{x(b2):.1f}%"></i></span>'
                f'<span class="val">{pct(a, L)} → <b>{pct(b2, L)}</b></span></div>')
    ticks = ''.join(f'<i style="left:{x(v):.1f}%">{pct(v, L) if v else "0"}</i>' for v in range(lo, hi + 1, 20 if hi - lo > 60 else 10))
    out += f'<div class="db ax"><span class="name"></span><span class="trk">{ticks}</span><span class="val"></span></div>'
    if L == 'vi':
        legend = '<span><i class="k0"></i>ngày báo cáo</span><span><i class="k1"></i>hiện tại</span><span><i class="k1 m"></i>mục tiêu cũ hoặc bị báo hạ</span>'
        axis = 'Khoảng cách = giá mục tiêu ÷ giá − 1, cùng một giá mục tiêu ở cả hai điểm.'
    else:
        legend = '<span><i class="k0"></i>report date</span><span><i class="k1"></i>now</span><span><i class="k1 m"></i>old or flagged target</span>'
        axis = 'Gap = target ÷ price − 1, with the same target at both points.'
    aria = '; '.join(f'{re.sub("<[^>]+>", "", r[0])} {pct(r[1], L)} to {pct(r[2], L)}' for r in rows)
    return chart_fig(title, sub, legend, out, axis, cap_extra, aria, cls)

def progress_chart(ts, L, title, sub):
    rows = sorted([t for t in ts if t.get('prog')], key=lambda t: -t['prog']['pct'])
    if not rows: return ''
    hi = 125
    out = ''
    for t in rows:
        g = t['prog']; w = min(g['pct'], hi) / hi * 100
        basis = ('kế hoạch công ty' if g['basis'] == 'company' else 'dự báo Mirae Asset') if L == 'vi' else ('company target' if g['basis'] == 'company' else 'Mirae Asset forecast')
        met = {'PBT': ('LNTT', 'PBT'), 'NPAT': ('LNST', 'net profit')}[g['metric']][0 if L == 'vi' else 1]
        v = ('≈' if g.get('computed') else '') + num(g['pct'], L, 1 if g['pct'] % 1 else 0) + '%'
        tip = f'{t["ticker"]}: {met} 9M26 = {v} {basis}'
        out += (f'<div class="barrow pg" tabindex="0" data-tip="{E(tip)}"><span class="name">{t["ticker"]}</span><span class="track"><i class="pace" style="left:{75 / hi * 100:.1f}%"></i>'
                f'<span class="bar{" soft" if g["basis"] == "company" else ""}" style="width:{w:.1f}%"></span></span><span class="val">{v}</span></div>')
    if L == 'vi':
        legend = '<span><i style="background:var(--series-1)"></i>so với dự báo Mirae Asset</span><span><i style="background:var(--series-1-soft)"></i>so với kế hoạch của công ty</span><span><i class="pk"></i>75%: đúng nhịp sau 3 quý</span>'
        axis = f'0% ── {hi}% · ≈: tự tính từ hai con số Mirae Asset in, báo cáo không in tỷ lệ'
        cap = 'LNTT với ngân hàng, FPT và GMD; LNST với các mã còn lại. ' + E(SC['progress_other']['vi'])
    else:
        legend = '<span><i style="background:var(--series-1)"></i>against Mirae Asset forecast</span><span><i style="background:var(--series-1-soft)"></i>against company target</span><span><i class="pk"></i>75%: on pace after three quarters</span>'
        axis = f'0% ── {hi}% · ≈: calculated from two figures Mirae Asset prints; the report does not print the ratio'
        cap = 'Pre-tax profit for banks, FPT and GMD; net profit for the rest. ' + E(SC['progress_other']['en'])
    aria = ', '.join(f'{t["ticker"]} {num(t["prog"]["pct"], L, 1)}%' for t in rows)
    return chart_fig(title, sub, legend, out, axis, cap, aria)

def coverage_chart(ts, L):
    rows = sorted([t for t in ts if t.get('cov')], key=lambda t: -t['cov']['pct'])
    if not rows: return ''
    hi = 250; out = ''
    for t in rows:
        c = t['cov']; w = c['pct'] / hi * 100
        out += (f'<div class="barrow pg" tabindex="0" data-tip="{E(t["ticker"] + ": " + num(c["pct"], L, 1) + "% (" + c["when"] + ")")}"><span class="name">{t["ticker"]}</span>'
                f'<span class="track"><i class="pace" style="left:{100 / hi * 100:.1f}%"></i><span class="bar{" soft" if c["pct"] < 100 else ""}" style="width:{w:.1f}%"></span></span>'
                f'<span class="val">{num(c["pct"], L, 0)}%</span></div>')
    if L == 'vi':
        title, sub = 'Tỷ lệ bao phủ nợ xấu', 'Dự phòng rủi ro tín dụng ÷ nợ xấu, % · vạch: 100% · thanh nhạt: dưới 100%'
        cap = 'Cuối 3Q26, trừ TPB (1Q26), STB và EIB (cuối 2025): các mã này không có báo cáo mới hơn. Mirae Asset ước tính toàn ngành khoảng 79%, so với 106-143% ở đầu chu kỳ trước.'
    else:
        title, sub = 'Loan-loss coverage', 'Loan-loss reserves ÷ bad debt, % · line: 100% · light bars: below 100%'
        cap = 'End-3Q26, except TPB (1Q26), STB and EIB (end-2025): no later reports for these. Mirae Asset puts the sector at about 79%, against 106-143% at the start of the last cycle.'
    aria = ', '.join(f'{t["ticker"]} {num(t["cov"]["pct"], L, 0)}%' for t in rows)
    return chart_fig(title, sub, '', out, '0% ── 250%', cap, aria)

def scorecard(ts, L, link=None, with_ind=False):
    if L == 'vi':
        th = ['Mã'] + (['Ngành'] if with_ind else []) + ['Khuyến nghị', 'Giá mục tiêu', 'Giá hiện tại', 'Khoảng cách: ngày báo cáo', 'Khoảng cách: hiện tại', 'Lợi nhuận 9T26', 'Bảng cân đối', 'P/E', 'P/B']
    else:
        th = ['Ticker'] + (['Industry'] if with_ind else []) + ['Rating', 'Target', 'Price now', 'Gap at report', 'Gap now', '9M26 profit', 'Balance sheet', 'P/E', 'P/B']
    txtcols = {th[0], 'Ngành', 'Industry', 'Khuyến nghị', 'Rating', 'Bảng cân đối', 'Balance sheet'}
    h = ''.join(f'<th>{E(c)}</th>' if c in txtcols else f'<th class="num">{E(c)}</th>' for c in th)
    rows = ''
    for t in ts:
        k = t['ticker']; href = link(t) if link else f'#{k}'
        r = f'<td><a href="{href}">{k}</a></td>'
        if with_ind: r += f'<td class="t">{E(T(t["page_label"], L))}</td>'
        r += f'<td data-v="{["Sell", "Hold", "Trading Buy", "Buy"].index(t["rating"]) if t.get("rating") in ("Sell", "Hold", "Trading Buy", "Buy") else -1}">{pick(t.get("rating"), L)}</td>'
        r += (f'<td class="num" data-v="{t["tp"]}">{num(t["tp"], L)}<span class="sub">{fdate(t["tp_date"], L)}</span></td>' if t.get('tp') else '<td class="num" data-v="">–</td>')
        r += f'<td class="num" data-v="{t["px"]}">{num(t["px"], L)}</td>'
        r += (f'<td class="num" data-v="{t["gap_then"]:.1f}">{pct(t["gap_then"], L)}</td>' if t['gap_then'] is not None else '<td class="num" data-v="">–</td>')
        r += gap_cell(t, L)
        g = t.get('prog')
        r += (f'<td class="num" data-v="{g["pct"]}">{"≈" if g.get("computed") else ""}{num(g["pct"], L, 1 if g["pct"] % 1 else 0)}%<span class="sub">{("kế hoạch" if L == "vi" else "co. target") if g["basis"] == "company" else ""}</span></td>' if g else '<td class="num" data-v="">–</td>')
        r += bs_cell(t, L)
        r += (f'<td class="num" data-v="{t["pe"]}">{mult(t["pe"], L)}</td>' if 0 < t['pe'] < 60 else '<td class="num" data-v="">n/m</td>')
        r += f'<td class="num" data-v="{t["pb"]}">{num(t["pb"], L, 2)}x</td>'
        rows += f'<tr>{r}</tr>'
    return f'<div class="tablewrap"><table class="sort sc"><thead><tr>{h}</tr></thead><tbody>{rows}</tbody></table></div>'

def scorecard_note(L):
    X = TXT[L]
    if L == 'vi':
        return (f'<p class="note2">Giá mục tiêu, khuyến nghị và khoảng cách ngày báo cáo theo báo cáo Mirae Asset ghi dưới giá mục tiêu (có thể là báo cáo nhanh nhắc lại mục tiêu cũ). '
                f'Giá hiện tại: phiên sáng {fdate(PRICE_DATE, L)}; P/E, P/B 4 quý gần nhất theo giá thị trường ngày {fdate(VAL_DATE, L)} (FiinQuantX). '
                f'Lợi nhuận 9T26: % của dự báo cả năm của Mirae Asset, hoặc của kế hoạch công ty nếu ghi "kế hoạch"; ≈ là tự tính. Bảng cân đối: ngân hàng theo tỷ lệ bao phủ nợ xấu; doanh nghiệp khác theo tiền mặt và nợ. '
                f'* {X["stale"]}. † {X["review"]}. Bấm tiêu đề cột để sắp xếp.</p>')
    return (f'<p class="note2">Target, rating and gap at report come from the Mirae Asset report dated under the target (this can be a results flash restating an older target). '
            f'Price now: morning session of {fdate(PRICE_DATE, L)}; P/E and P/B are trailing four quarters at market price as of {fdate(VAL_DATE, L)} (FiinQuantX). '
            f'9M26 profit: % of Mirae Asset\'s full-year forecast, or of the company target where marked; ≈ is calculated. Balance sheet: banks by loan-loss coverage; others by cash against debt. '
            f'* {X["stale"]}. † {X["review"]}. Click a column heading to sort.</p>')

def ticker_block(t, L):
    X = TXT[L]; k = t['ticker']
    name = t['name_vi'] if L == 'vi' else t['name_en']
    if t.get('tp'):
        line = f'{X["target"]} {num(t["tp"], L)} ({fdate(t["tp_date"], L)}) · {X["price"]} {num(t["px"], L)} · {X["gap"]} <span class="{"old" if t["flag"] else cls(t["gap"])}">{pct(t["gap"], L)}</span>{t["flag"]}'
    else:
        line = f'{X["none_tp"]} · {X["price"]} {num(t["px"], L)}'
    g = t.get('prog')
    if g:
        line += (f' · {"lợi nhuận 9T26" if L == "vi" else "9M26 profit"} {"≈" if g.get("computed") else ""}{num(g["pct"], L, 1 if g["pct"] % 1 else 0)}%')
    line += f' · {E(BS_TXT[L][bs_key(t)])}'
    line += f' · P/E {mult(t["pe"], L) if 0 < t["pe"] < 60 else "n/m"} · P/B {num(t["pb"], L, 2)}x'
    note = T(t['tp_note'], L).strip() if t.get('tp_note') else ''
    ul = lambda items: '<ul>' + ''.join(f'<li>{E(T(i, L))}</li>' for i in items) + '</ul>'
    ms = '<ul>' + ''.join(ms_li(m, L) for m in sorted(t['milestones'], key=lambda m: ms_sort(m['when']))) + '</ul>'
    src = ' · '.join(f'<a href="{E(s["url"])}">{E(s["title_short"])}</a> ({fdate(s["date"], L)})' for s in t['sources'])
    return (f'<details class="tk" id="{k}"><summary><h3><span class="sym">{k}</span><span class="nm">{E(name)}</span>{pick(t.get("rating"), L)}</h3>'
            f'<p class="tkline">{line}</p><p class="thesis">{E(T(t["thesis"], L))}</p></summary>'
            + (f'<p class="note2">* {E(note)}</p>' if note else '') +
            f'<div class="tri"><div><h4>{X["drivers"]}</h4>{ul(t["drivers"])}</div><div><h4>{X["milestones"]}</h4>{ms}</div><div><h4>{X["cushion"]}</h4>{ul(t["cushion"])}</div></div>'
            f'<p class="brk"><strong>{X["breaks"]}:</strong> {E(T(t["breaks"], L))}</p>'
            f'<p class="src">{X["sources"]}: {src}</p></details>')

def toggles(L):
    a, b = ('Mở tất cả', 'Thu gọn tất cả') if L == 'vi' else ('Expand all', 'Collapse all')
    return f'<p class="tog"><button type="button" data-all="1">{a}</button><button type="button" data-all="0">{b}</button></p>'

def med(v):
    v = [x for x in v if x is not None]
    return statistics.median(v) if v else None

def dumbbell_stocks(ts, L, title, sub):
    rows = []
    for t in sorted([t for t in ts if t['gap'] is not None and t['gap_then'] is not None], key=lambda t: -t['gap']):
        tip = (f'{t["ticker"]}: {num(t["price_at_tp_date"], L)} → {num(t["px"], L)}; {X_TARGET[L]} {num(t["tp"], L)} ({fdate(t["tp_date"], L)})')
        rows.append((t['ticker'] + t['flag'], t['gap_then'], t['gap'], bool(t['flag']), tip))
    return dumbbell(rows, L, title, sub)
X_TARGET = {'vi': 'mục tiêu', 'en': 'target'}

def industry_page(P, L):
    X = TXT[L]
    ts = [TK[k] for k in P['tickers']]
    n_reports = len({s['url'] for t in ts for s in t['sources']} | {s['url'] for g in P['segments'] for s in D['segments'][g].get('sources', [])})
    hdg = P['h2'][L]
    b = crumb(P['slug'], L) + f'<h1>{E(T(P["title"], L))}</h1><p class="dek">{E(T(P["dek"], L))}</p>' + byline(P, ts, L, n_reports)
    b += tiles(P['tiles'], L) + keypoints(P, L) + how_to_read(L)
    b += f'<h2>1 · {E(hdg[0])}</h2>' + ''.join(segment_block(D['segments'][g], L, i, single=len(P['segments']) == 1) for i, g in enumerate(P['segments']))
    b += f'<h2>2 · {E(hdg[1])}</h2><p>{rich(T(P["cushion_text"], L))}</p>'
    t1, s1 = T(P['chart'], L)
    b += '<div class="grid2">' + dumbbell_stocks(ts, L, t1, s1)
    pt = ('Lợi nhuận đã ghi nhận sau 9 tháng', '% của con số cả năm 2026') if L == 'vi' else ('Profit booked after nine months', '% of the full-year 2026 figure')
    b += (coverage_chart(ts, L) if any(t.get('cov') for t in ts) else '') + progress_chart(ts, L, *pt) + '</div>'
    b += scorecard(sorted(ts, key=lambda t: -(t['gap'] if t['gap'] is not None else -999)), L) + scorecard_note(L)
    b += f'<h2>3 · {E(hdg[2])}</h2>' + toggles(L) + ''.join(ticker_block(t, L) for t in ts)
    back = ('<p style="margin-top:36px"><a href="../mirae-asset-11-2026/">← Tổng quan 44 cổ phiếu và lịch mốc theo dõi</a></p>' if L == 'vi'
            else '<p style="margin-top:36px"><a href="../../mirae-asset-11-2026/en/">← Overview of all 44 tickers and the milestone calendar</a></p>')
    b += back + disclaimer(L, n_reports)
    write(P['slug'], L, shell(L, P['slug'], T(P['title'], L), T(P['dek'], L), b))

def industry_summary(pages, L, link_pg):
    if L == 'vi':
        th = ['Ngành', 'Quan điểm của Mirae Asset', 'Số mã', 'Khoảng cách trung vị (mục tiêu mới)', 'Lợi nhuận 9T26 trung vị', 'Bộ đệm bảng cân đối dày', 'Mục tiêu cần trừ hao']
    else:
        th = ['Industry', 'Mirae Asset stance', 'Stocks', 'Median gap (recent targets)', 'Median 9M26 profit', 'Strong balance sheet', 'Targets to discount']
    h = ''.join(f'<th{" class=num" if 2 <= i <= 4 else ""}>{E(c)}</th>' for i, c in enumerate(th))
    rows = ''
    for pg in pages:
        ts = [TK[k] for k in pg['tickers']]
        fr = [t['gap'] for t in ts if t['fresh']]
        mg = med(fr); mp = med([t['prog']['pct'] for t in ts if t.get('prog')])
        strong = [t['ticker'] for t in ts if BS_RANK[bs_key(t)] >= 4]
        fl = [t['ticker'] + t['flag'] for t in ts if t['flag']]
        rows += (f'<tr><td><a href="{link_pg(pg)}">{E(T(pg["label"], L))}</a></td><td class="t">{E(T(pg["stance"], L))}</td><td class="num">{len(ts)}</td>'
                 f'<td class="num" data-v="{mg if mg is not None else ""}">{pct(mg, L) if mg is not None else "–"}<span class="sub">n={len(fr)}</span></td>'
                 f'<td class="num">{num(mp, L, 0) + "%" if mp is not None else "–"}</td>'
                 f'<td class="t lst"><b>{len(strong)}/{len(ts)}</b> {" ".join(strong)}</td>'
                 f'<td class="t lst"><b>{len(fl)}</b> {" ".join(fl)}</td></tr>')
    return f'<div class="tablewrap"><table class="sum"><thead><tr>{h}</tr></thead><tbody>{rows}</tbody></table></div>'

def overview_page(L):
    X = TXT[L]; P = META['overview']
    pages = META['pages']
    ts = []
    for pg in pages:
        for k in pg['tickers']:
            TK[k]['page_label'] = pg['label']; TK[k]['page_slug'] = pg['slug']; ts.append(TK[k])
    n_reports = len({s['url'] for t in ts for s in t['sources']} | {s['url'] for g in D['segments'].values() for s in g.get('sources', [])})
    link = lambda t: (f'../{t["page_slug"]}/#{t["ticker"]}' if L == 'vi' else f'../../{t["page_slug"]}/en/#{t["ticker"]}')
    link_pg = lambda pg: (f'../{pg["slug"]}/' if L == 'vi' else f'../../{pg["slug"]}/en/')
    hdg = P['h2'][L]
    b = crumb(P['slug'], L) + f'<h1>{E(T(P["title"], L))}</h1><p class="dek">{E(T(P["dek"], L))}</p>' + byline(P, ts, L, n_reports)
    b += tiles(P['tiles'], L) + keypoints(P, L) + how_to_read(L)
    # 1 industry summary
    b += f'<h2>1 · {E(hdg[0])}</h2><p>{rich(T(P["summary_text"], L))}</p>' + industry_summary(pages, L, link_pg)
    # 2 gaps then vs now, by industry (recent targets only) + 9M progress
    rows = []
    for pg in pages:
        fr = [TK[k] for k in pg['tickers'] if TK[k]['fresh']]
        if not fr: continue
        a, c = med([t['gap_then'] for t in fr]), med([t['gap'] for t in fr])
        rows.append((f'<a href="{link_pg(pg)}">{E(T(pg["label"], L))}</a>', a, c, False, f'{T(pg["label"], L)}: n={len(fr)}'))
    allf = [t for t in ts if t['fresh']]
    rows.append(('<b>' + ('Tất cả' if L == 'vi' else 'All') + '</b>', med([t['gap_then'] for t in allf]), med([t['gap'] for t in allf]), False, f'n={len(allf)}'))
    t2 = (('Khoảng cách trung vị đến mục tiêu: ngày báo cáo và hiện tại', f'Chỉ các mục tiêu mới và không bị báo hạ ({len(allf)} mã), theo ngành') if L == 'vi'
          else ('Median gap to target: at the report date and now', f'Recent targets not flagged for a cut only ({len(allf)} stocks), by industry'))
    pt = ('Lợi nhuận đã ghi nhận sau 9 tháng', '% của con số cả năm 2026, 34 mã có số liệu') if L == 'vi' else ('Profit booked after nine months', '% of the full-year 2026 figure, 34 stocks with data')
    b += f'<h2>2 · {E(hdg[1])}</h2><p>{rich(T(P["cushion_text"], L))}</p>'
    b += dumbbell(rows, L, *t2, cls='ind solo') + progress_chart(ts, L, *pt)
    # 3 scorecard
    b += f'<h2>3 · {E(hdg[2])}</h2><p>{rich(T(P["scorecard_text"], L))}</p>'
    b += scorecard(sorted(ts, key=lambda t: -(t['gap'] if t['gap'] is not None else -999)), L, link=link, with_ind=True) + scorecard_note(L)
    # 4 calendar
    b += f'<h2>4 · {E(hdg[3])}</h2><p>{rich(T(P["calendar_text"], L))}</p><div class="cal">'
    items = [(m, t['ticker']) for t in ts for m in t['milestones']]
    for bk in ['4Q26', 'fy26', '1Q27', '2Q27', '2H27', 'later', 'pending', 'passed']:
        sel = sorted([x for x in items if bucket(x[0]['when']) == bk], key=lambda x: (ms_sort(x[0]['when']), x[1]))
        if not sel: continue
        lis = ''.join(ms_li(m, L, sym=f'<a href="{link(TK[k])}">{k}</a>') for m, k in sel)
        b += f'<details class="more"{" open" if bk == "4Q26" else ""}><summary>{E(X["bucket"][bk])} ({len(sel)})</summary><ul>{lis}</ul></details>'
    b += '</div>'
    # 5 industry reports
    b += f'<h2>5 · {E(hdg[4])}</h2><div class="cards">'
    for pg in pages:
        b += (f'<a class="card" href="{link_pg(pg)}"><p class="label">{X["kick"]} · {E(T(pg["label"], L))}</p><h3>{E(T(pg["title"], L))}</h3><p class="sum">{E(T(pg["dek"], L))}</p>'
              f'<p class="meta">{" · ".join(pg["tickers"])}</p></a>')
    b += '</div>'
    # 6 method
    b += f'<h2>6 · {E(hdg[5])}</h2>' + ''.join(f'<p>{rich(x)}</p>' for x in P['method'][L])
    b += disclaimer(L, n_reports)
    write(P['slug'], L, shell(L, P['slug'], T(P['title'], L), T(P['dek'], L), b))

# ---------- index cards: idempotent, so a vault copy-in that rewrites the indexes can be repaired by re-running ----------
MARK = '<!-- mirae-coverage -->'
def card(href, label, title, dek, meta):
    return (f'<a class="card" href="{href}">{MARK}<p class="label">{E(label)}</p><h3>{E(title)}</h3>'
            f'<p class="sum">{E(dek)}</p><p class="meta">{E(meta)}</p></a>\n')
def put_cards(path, anchor, cards):
    """Insert our cards right after `anchor`, replacing any copies from an earlier run. Returns True if the index changed."""
    f = os.path.join(ROOT, path)
    if not os.path.exists(f): print('  skip (missing):', path); return False
    h = open(f, encoding='utf-8').read()
    clean = re.sub(r'<a class="card" href="[^"]*">' + re.escape(MARK) + r'.*?</a>\n', '', h, flags=re.S)
    # cards added by hand before the marker existed
    clean = re.sub(r'<a class="card" href="[^"]*mirae[^"]*">(?:(?!</a>).)*</a>\n', '', clean, flags=re.S)
    # anchor = the section heading; cards go right after the first card grid that follows it
    i = clean.find(anchor)
    j = clean.find('<div class="cards">\n', i) if i >= 0 else -1
    if j < 0: print('  WARNING: anchor not found, cards not placed in', path); return False
    j += len('<div class="cards">\n')
    new = clean[:j] + ''.join(cards) + clean[j:]
    if new != h: open(f, 'w', encoding='utf-8').write(new)
    return new != h
def index_cards():
    ov, pages = META['overview'], META['pages']
    d_vi, d_en = fdate(PUB, 'vi'), fdate(PUB, 'en')
    out = {
      'index.html': put_cards('index.html', '<h2 class="section" id="nganh">',
            [card('nganh/' + ov['slug'] + '/', 'Báo cáo ngành · Mirae Asset', ov['title']['vi'], ov['dek']['vi'], d_vi + ' · 6 báo cáo ngành')]),
      'en/index.html': put_cards('en/index.html', '<h2 class="section" id="nganh">',
            [card('../nganh/' + ov['slug'] + '/en/', 'Sector report · Mirae Asset', ov['title']['en'], ov['dek']['en'], d_en + ' · six industry reports')]),
    }
    for k, v in out.items(): print('  index', k, 'updated' if v else 'already current')

if __name__ == '__main__':
    for pg in META['pages']:
        for k in pg['tickers']: TK[k]['page_label'] = pg['label']; TK[k]['page_slug'] = pg['slug']
    for L in ('vi', 'en'):
        for pg in META['pages']: industry_page(pg, L)
        overview_page(L)
    whens = sorted({m['when'] for t in D['tickers'] for m in t['milestones']} | {m['when'] for s in D['segments'].values() for m in s['milestones']})
    if '--whens' in sys.argv:
        for w in whens: print(f'{w!r:45} -> {when_vi(w)!r:40} {bucket(w)}')
    print('built', len(META['pages']) + 1, 'pages x 2 languages;', len(D['tickers']), 'tickers')
    if '--no-index' not in sys.argv:
        index_cards()
        # the industry section (/nganh/, /nganh/en/, homepage industry row, 'same industry' links) is owned by tools/industry-index
        import subprocess
        subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'industry-index', 'build.py')], check=True)
