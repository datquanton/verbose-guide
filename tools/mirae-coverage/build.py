#!/usr/bin/env python3
"""Build the Mirae Asset coverage pages (milestones, drivers, cushion) into /nganh/.

Inputs (this folder):  data.json   per-ticker reading of Mirae Asset Vietnam reports (see README.md)
                       market.json prices and trailing multiples from FiinQuantX
                       meta.json   hand-written titles, key points and tiles for each page
Run:  python3 tools/mirae-coverage/build.py      (from the repository root)
"""
import json, os, re, html, statistics, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))
MK = json.load(open(os.path.join(HERE, 'market.json'), encoding='utf-8'))
META = json.load(open(os.path.join(HERE, 'meta.json'), encoding='utf-8'))
WHENS = json.load(open(os.path.join(HERE, 'whens.json'), encoding='utf-8'))   # milestone label -> [Vietnamese label, calendar bucket]
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

TXT = {
 'vi': dict(site='Nghiên cứu cổ phiếu Việt Nam', nav=[('vi-mo/', 'Vĩ mô'), ('nganh/', 'Ngành'), ('ket-qua-kinh-doanh/', 'Kết quả kinh doanh')],
   other='English', theme='Đổi giao diện sáng/tối', pub='Công bố', kick='Báo cáo ngành', keypoints='Điểm chính',
   foot='Nghiên cứu cá nhân, không phải khuyến nghị đầu tư. Quan điểm là của riêng tác giả và có thể thay đổi mà không cần báo trước.',
   drivers='Động lực cốt lõi', milestones='Mốc theo dõi', cushion='Bộ đệm', breaks='Điều gì phá vỡ luận điểm', sources='Báo cáo đã đọc',
   target='Giá mục tiêu', price='giá', gap='khoảng cách đến giá mục tiêu', none_tp='Mirae Asset không nêu giá mục tiêu trong các báo cáo gần nhất',
   th=['Mã', 'Khuyến nghị', 'Giá mục tiêu', 'Ngày báo cáo', 'Giá khi đó', 'Giá hiện tại', 'Từ ngày báo cáo', 'Đến giá mục tiêu', 'Biên an toàn', 'P/E', 'P/B'],
   ind='Ngành', when='Khi nào', what='Điều cần thấy', stale='giá mục tiêu đặt hơn 100 ngày trước', review='Mirae Asset đã báo sẽ hạ dự báo hoặc định giá', nodata='–',
   bucket={'passed': 'Vừa qua', '4Q26': 'Từ nay đến hết 2026: sự kiện có thời điểm', 'fy26': 'Kiểm chứng cả năm 2026', '1Q27': 'Đầu 2027 (1Q27, 1H27)', '2Q27': 'Quý 2/2027', '2H27': 'Phần còn lại của 2027', 'later': 'Từ 2028 trở đi', 'pending': 'Chưa có ngày hoặc chờ xác nhận'}),
 'en': dict(site='Vietnam Equity Research', nav=[('en/#vi-mo', 'Macro'), ('en/#nganh', 'Sectors'), ('en/#ket-qua-kinh-doanh', 'Earnings')],
   other='Tiếng Việt', theme='Switch light/dark theme', pub='Published', kick='Sector report', keypoints='Key points',
   foot="Personal research, not investment advice. Views are the author's own and may change without notice.",
   drivers='Underlying drivers', milestones='Milestones', cushion='Cushion', breaks='What breaks the thesis', sources='Reports read',
   target='Target price', price='price', gap='gap to target', none_tp='Mirae Asset states no target price in its latest notes',
   th=['Ticker', 'Rating', 'Target', 'Report date', 'Price then', 'Price now', 'Since report', 'Gap to target', 'Margin of safety', 'P/E', 'P/B'],
   ind='Industry', when='When', what='What to see', stale='target set more than 100 days ago', review='Mirae Asset has said it will likely cut forecasts or valuation', nodata='–',
   bucket={'passed': 'Just passed', '4Q26': 'From now to end-2026: dated events', 'fy26': 'Full-year 2026 checks', '1Q27': 'Early 2027 (1Q27, 1H27)', '2Q27': '2Q27', '2H27': 'Rest of 2027', 'later': '2028 onwards', 'pending': 'Undated or awaiting confirmation'}),
}

CSS = """
.tk{border-top:1px solid var(--grid);margin-top:34px;padding-top:6px}
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
.pick{white-space:nowrap}
"""
SORT_JS = """<script>document.querySelectorAll('table.sort').forEach(function(tb){var ths=tb.querySelectorAll('th');ths.forEach(function(th,i){th.addEventListener('click',function(){
var body=tb.tBodies[0],rows=[].slice.call(body.rows),dir=th.getAttribute('aria-sort')==='descending'?1:-1;ths.forEach(function(h){h.removeAttribute('aria-sort')});
th.setAttribute('aria-sort',dir<0?'descending':'ascending');rows.sort(function(a,b){var x=a.cells[i].dataset.v,y=b.cells[i].dataset.v;
if(x===undefined){return dir*a.cells[i].textContent.localeCompare(b.cells[i].textContent)}x=x===''?-1e18:+x;y=y===''?-1e18:+y;return dir*(x-y)});
rows.forEach(function(r){body.appendChild(r)})})})});</script>"""
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
            f'<main class="wrap">\n{body}\n{SORT_JS}\n</main>\n'
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

def table(ts, L, link=None, with_ind=False):
    X = TXT[L]; th = X['th']
    cols = [th[0]] + ([X['ind']] if with_ind else []) + th[1:]
    numcol = lambda c: c not in (th[0], th[1], X['ind'])
    h = ''.join(f'<th class="num">{E(c)}</th>' if numcol(c) else f'<th>{E(c)}</th>' for c in cols)
    rows = []
    for t in ts:
        k = t['ticker']
        href = (link(t) if link else f'#{k}')
        r = f'<td><a href="{href}">{k}</a></td>'
        if with_ind: r += f'<td class="t">{E(T(t["page_label"], L))}</td>'
        r += f'<td>{pick(t.get("rating"), L)}</td>'
        if t.get('tp'):
            r += f'<td class="num" data-v="{t["tp"]}">{num(t["tp"], L)}</td><td class="num" data-v="{t["tp_date"].replace("-", "")}">{fdate(t["tp_date"], L)}</td>'
            r += (f'<td class="num" data-v="{t["price_at_tp_date"]}">{num(t["price_at_tp_date"], L)}</td>' if t.get('price_at_tp_date') else '<td class="num" data-v="">–</td>')
        else:
            r += '<td class="num" data-v="">–</td>' + f'<td class="num" data-v="{t["latest_report_date"].replace("-", "")}">{fdate(t["latest_report_date"], L)}</td>' + '<td class="num" data-v="">–</td>'
        r += f'<td class="num" data-v="{t["px"]}">{num(t["px"], L)}</td>'
        r += (f'<td class="num" data-v="{t["since"]:.1f}"><span class="{cls(t["since"])}">{pct(t["since"], L)}</span></td>' if t['since'] is not None else '<td class="num" data-v="">–</td>')
        r += gap_cell(t, L)
        r += (f'<td class="num" data-v="{t["absorb"]:.1f}">{pct(t["absorb"], L, sign=False)}</td>' if t['absorb'] is not None else '<td class="num" data-v="">–</td>')
        r += (f'<td class="num" data-v="{t["pe"]}">{mult(t["pe"], L)}</td>' if 0 < t['pe'] < 60 else f'<td class="num" data-v="">{"n/m"}</td>')
        r += f'<td class="num" data-v="{t["pb"]}">{num(t["pb"], L, 2)}x</td>'
        rows.append(f'<tr>{r}</tr>')
    return f'<div class="tablewrap"><table class="sort"><thead><tr>{h}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'

def table_note(L):
    X = TXT[L]
    if L == 'vi':
        return (f'<p class="note2">Giá mục tiêu, khuyến nghị và "giá khi đó" lấy từ báo cáo Mirae Asset ở ngày ghi trong bảng (có thể là báo cáo nhanh nhắc lại mục tiêu cũ; ghi chú dưới từng mã cho biết mục tiêu được đặt khi nào). '
                f'Giá hiện tại là giá phiên sáng {fdate(PRICE_DATE, L)}; P/E và P/B là 4 quý gần nhất theo giá thị trường, ngày {fdate(VAL_DATE, L)} (FiinQuantX). '
                f'Biên an toàn = 1 − giá hiện tại ÷ giá mục tiêu: giá trị Mirae Asset ước tính có thể giảm bao nhiêu trước khi bằng giá hiện tại. '
                f'* {X["stale"]}. † {X["review"]}. Với hai nhóm này, khoảng cách đến mục tiêu không nên đọc như bộ đệm. Bấm vào tiêu đề cột để sắp xếp.</p>')
    return (f'<p class="note2">Target, rating and "price then" come from the Mirae Asset report dated in the table (this can be a results flash restating an older target; the note under each ticker says when the target was set). '
            f'Price now is the morning session of {fdate(PRICE_DATE, L)}; P/E and P/B are trailing four quarters at market price, as of {fdate(VAL_DATE, L)} (FiinQuantX). '
            f'Margin of safety = 1 − price now ÷ target: how far Mirae Asset\'s estimate of value could fall before it equals today\'s price. '
            f'* {X["stale"]}. † {X["review"]}. For both groups, do not read the gap to target as cushion. Click a column heading to sort.</p>')

def gap_chart(ts, L, title, sub):
    rows = [t for t in ts if t['gap'] is not None]
    rows.sort(key=lambda t: -t['gap'])
    if not rows: return ''
    mx = max(max(t['gap'] for t in rows), 10)
    scale = (int(mx / 20) + 1) * 20
    b = ''
    for t in rows:
        w = max(t['gap'], 0) / scale * 100
        tip = f'{t["ticker"]}: {num(t["px"], L)} → {num(t["tp"], L)} ({fdate(t["tp_date"], L)})'
        soft = ' soft' if t['flag'] else ''
        b += (f'<div class="barrow" title="{E(tip)}"><span class="name">{t["ticker"]}{t["flag"]}</span><span class="track"><span class="bar{soft}" style="width:{w:.1f}%"></span></span>'
              f'<span class="val{" down" if t["gap"] < 0 else ""}">{pct(t["gap"], L)}</span></div>')
    aria = ', '.join(f'{t["ticker"]} {pct(t["gap"], L)}' for t in rows)
    axis = (f'0% ── {scale}% · thanh nhạt: * {TXT[L]["stale"]}; † {TXT[L]["review"]}' if L == 'vi' else f'0% ── {scale}% · lighter bars: * {TXT[L]["stale"]}; † {TXT[L]["review"]}')
    cap = (f'Giá mục tiêu: báo cáo Mirae Asset gần nhất có nêu mục tiêu. Giá: phiên sáng {fdate(PRICE_DATE, L)}, FiinQuantX. Khoảng cách âm hiển thị bằng số, không có thanh.' if L == 'vi'
           else f'Targets: the latest Mirae Asset report that states one. Prices: morning session of {fdate(PRICE_DATE, L)}, FiinQuantX. Negative gaps are shown as a number with no bar.')
    return (f'<figure class="viz"><p class="viz-title">{E(title)}</p><p class="viz-sub">{E(sub)}</p><div role="img" aria-label="{E(aria)}">{b}</div>'
            f'<div class="axis-note">{E(axis)}</div><figcaption>{E(cap)}</figcaption></figure>')

def ms_li(m, L, sym=None):
    past = bucket(m['when']) == 'passed'
    s = f'<span class="sym">{sym}</span>' if sym else ''
    return f'<li>{s}<span class="when{" past" if past else ""}">{E(when_lbl(m["when"], L))}</span> {E(T(m, L))}</li>'

def ticker_block(t, L):
    X = TXT[L]; k = t['ticker']
    name = t['name_vi'] if L == 'vi' else t['name_en']
    if t.get('tp'):
        line = f'{X["target"]} {num(t["tp"], L)} ({fdate(t["tp_date"], L)}) · {X["price"]} {num(t["px"], L)} · {X["gap"]} <span class="{"old" if t["flag"] else cls(t["gap"])}">{pct(t["gap"], L)}</span>{t["flag"]}'
    else:
        line = f'{X["none_tp"]} · {X["price"]} {num(t["px"], L)}'
    line += f' · P/E {mult(t["pe"], L) if 0 < t["pe"] < 60 else "n/m"} · P/B {num(t["pb"], L, 2)}x'
    f = t.get('forecast') or {}
    if f.get('fy26f') and f.get('growth_fy26f_pct') is not None:
        lab = {'PBT': ('LNTT', 'PBT'), 'NPAT': ('LNST', 'net profit')}.get(f.get('metric'), (f.get('metric', ''),) * 2)[0 if L == 'vi' else 1]
        yr = f.get('fy_label', '2026F')
        line += (f' · {lab} {yr}: {pct(f["growth_fy26f_pct"], L, 1)}' + (f', {f.get("fy_label_next", "2027F")}: {pct(f["growth_fy27f_pct"], L, 1)}' if f.get('growth_fy27f_pct') is not None else '')
                 + (' (dự báo Mirae Asset)' if L == 'vi' else ' (Mirae Asset forecast)'))
    note = T(t['tp_note'], L).strip() if t.get('tp_note') else ''
    ul = lambda items: '<ul>' + ''.join(f'<li>{E(T(i, L))}</li>' for i in items) + '</ul>'
    ms = '<ul>' + ''.join(ms_li(m, L) for m in sorted(t['milestones'], key=lambda m: ms_sort(m['when']))) + '</ul>'
    src = ' · '.join(f'<a href="{E(s["url"])}">{E(s["title_short"])}</a> ({fdate(s["date"], L)})' for s in t['sources'])
    return (f'<section class="tk" id="{k}"><h3><span class="sym">{k}</span><span class="nm">{E(name)}</span>{pick(t.get("rating"), L)}</h3>'
            f'<p class="tkline">{line}</p>' + (f'<p class="note2">* {E(note)}</p>' if note else '') +
            f'<p class="thesis">{E(T(t["thesis"], L))}</p>'
            f'<div class="tri"><div><h4>{X["drivers"]}</h4>{ul(t["drivers"])}</div><div><h4>{X["milestones"]}</h4>{ms}</div><div><h4>{X["cushion"]}</h4>{ul(t["cushion"])}</div></div>'
            f'<p class="brk"><strong>{X["breaks"]}:</strong> {E(T(t["breaks"], L))}</p>'
            f'<p class="src">{X["sources"]}: {src}</p></section>')

def segment_block(seg, L, n):
    X = TXT[L]
    out = f'<h3>{E(T(seg["name"], L))}</h3><p>{E(T(seg["view"], L))}</p>'
    out += '<ul>' + ''.join(f'<li>{E(T(d, L))}</li>' for d in seg['drivers']) + '</ul>'
    rows = ''.join(f'<tr><td><span class="when">{E(when_lbl(m["when"], L))}</span></td><td class="t">{E(T(m, L))}</td></tr>' for m in sorted(seg['milestones'], key=lambda m: ms_sort(m['when'])))
    out += f'<div class="tablewrap"><table><thead><tr><th>{X["when"]}</th><th>{X["what"]}</th></tr></thead><tbody>{rows}</tbody></table></div>'
    return out

def how_to_read(L):
    if L == 'vi':
        return ('<div class="callout"><p style="margin:0"><strong>Cách đọc.</strong> <strong>Động lực cốt lõi</strong> là vài biến số quyết định lợi nhuận của doanh nghiệp (sản lượng, giá bán, biên, chi phí vốn). '
                '<strong>Mốc theo dõi</strong> là sự kiện có ngày, kiểm chứng được, cho biết luận điểm còn đúng hướng hay không. <strong>Bộ đệm</strong> là thứ giới hạn mức giảm nếu động lực gây thất vọng: '
                'định giá, bảng cân đối, phần lợi nhuận đã chắc và cổ tức. Khoảng cách đến giá mục tiêu chỉ là một phần của bộ đệm, và chỉ có nghĩa khi mục tiêu còn mới.</p></div>')
    return ('<div class="callout"><p style="margin:0"><strong>How to read this.</strong> <strong>Underlying drivers</strong> are the few variables that set a company\'s earnings (volume, price, margin, funding cost). '
            '<strong>Milestones</strong> are dated, checkable events that show whether the thesis is still on track. <strong>Cushion</strong> is what limits the fall if the drivers disappoint: '
            'valuation, balance sheet, earnings already secured and dividends. The gap to target price is only one part of the cushion, and it means something only while the target is fresh.</p></div>')

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

def write(slug, L, htmltext):
    p = os.path.join(ROOT, 'nganh', slug, '' if L == 'vi' else 'en')
    os.makedirs(p, exist_ok=True)
    open(os.path.join(p, 'index.html'), 'w', encoding='utf-8').write(htmltext)

def industry_page(P, L):
    X = TXT[L]
    ts = [TK[k] for k in P['tickers']]
    n_reports = len({s['url'] for t in ts for s in t['sources']} | {s['url'] for g in P['segments'] for s in D['segments'][g].get('sources', [])})
    hdg = P['h2'][L]
    b = f'<p class="kicker">{X["kick"]} · {E(T(P["label"], L))}</p><h1>{E(T(P["title"], L))}</h1><p class="dek">{E(T(P["dek"], L))}</p>' + byline(P, ts, L, n_reports)
    b += tiles(P['tiles'], L) + keypoints(P, L) + how_to_read(L)
    b += '<div class="jump">' + ''.join(f'<a href="#{k}">{k}</a>' for k in P['tickers']) + '</div>'
    b += f'<h2>1 · {E(hdg[0])}</h2>' + ''.join(segment_block(D['segments'][g], L, i) for i, g in enumerate(P['segments']))
    b += f'<h2>2 · {E(hdg[1])}</h2><p>{rich(T(P["cushion_text"], L))}</p>'
    b += gap_chart(ts, L, *T(P['chart'], L)) + table(sorted(ts, key=lambda t: -(t['gap'] if t['gap'] is not None else -999)), L) + table_note(L)
    b += f'<h2>3 · {E(hdg[2])}</h2>' + ''.join(ticker_block(t, L) for t in ts)
    back = ('<p style="margin-top:36px"><a href="../mirae-asset-11-2026/">← Tổng quan 44 cổ phiếu và lịch mốc theo dõi</a></p>' if L == 'vi'
            else '<p style="margin-top:36px"><a href="../../mirae-asset-11-2026/en/">← Overview of all 44 tickers and the milestone calendar</a></p>')
    b += back + disclaimer(L, n_reports)
    write(P['slug'], L, shell(L, P['slug'], T(P['title'], L), T(P['dek'], L), b))

def overview_page(L):
    X = TXT[L]; P = META['overview']
    pages = META['pages']
    ts = []
    for pg in pages:
        for k in pg['tickers']:
            TK[k]['page_label'] = pg['label']; TK[k]['page_slug'] = pg['slug']; ts.append(TK[k])
    n_reports = len({s['url'] for t in ts for s in t['sources']} | {s['url'] for g in D['segments'].values() for s in g.get('sources', [])})
    link = lambda t: (f'../{t["page_slug"]}/#{t["ticker"]}' if L == 'vi' else f'../../{t["page_slug"]}/en/#{t["ticker"]}')
    b = f'<p class="kicker">{X["kick"]} · {E(T(P["label"], L))}</p><h1>{E(T(P["title"], L))}</h1><p class="dek">{E(T(P["dek"], L))}</p>' + byline(P, ts, L, n_reports)
    b += tiles(P['tiles'], L) + keypoints(P, L) + how_to_read(L)
    hdg = P['h2'][L]
    b += f'<h2>1 · {E(hdg[0])}</h2>' + ''.join(f'<p>{rich(x)}</p>' for x in P['method'][L])
    b += f'<h2>2 · {E(hdg[1])}</h2><p>{rich(T(P["cushion_text"], L))}</p>'
    b += table(sorted(ts, key=lambda t: -(t['gap'] if t['gap'] is not None else -999)), L, link=link, with_ind=True) + table_note(L)
    b += f'<h2>3 · {E(hdg[2])}</h2><p>{rich(T(P["calendar_text"], L))}</p><div class="cal">'
    items = [(m, t['ticker']) for t in ts for m in t['milestones']]
    for bk in ['4Q26', 'fy26', '1Q27', '2Q27', '2H27', 'later', 'pending', 'passed']:
        sel = sorted([x for x in items if bucket(x[0]['when']) == bk], key=lambda x: (ms_sort(x[0]['when']), x[1]))
        if not sel: continue
        lis = ''.join(ms_li(m, L, sym=f'<a href="{link(TK[k])}">{k}</a>') for m, k in sel)
        b += f'<details class="more"{" open" if bk == "4Q26" else ""}><summary>{E(X["bucket"][bk])} ({len(sel)})</summary><ul>{lis}</ul></details>'
    b += '</div>'
    b += f'<h2>4 · {E(hdg[3])}</h2><div class="cards">'
    for pg in pages:
        href = f'../{pg["slug"]}/' if L == 'vi' else f'../../{pg["slug"]}/en/'
        b += (f'<a class="card" href="{href}"><p class="label">{X["kick"]} · {E(T(pg["label"], L))}</p><h3>{E(T(pg["title"], L))}</h3><p class="sum">{E(T(pg["dek"], L))}</p>'
              f'<p class="meta">{" · ".join(pg["tickers"])}</p></a>')
    b += '</div>' + disclaimer(L, n_reports)
    write(P['slug'], L, shell(L, P['slug'], T(P['title'], L), T(P['dek'], L), b))

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
