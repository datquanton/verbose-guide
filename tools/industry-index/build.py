#!/usr/bin/env python3
"""Organise the industry section (/nganh/) by industry.

Input:  sections.json  registry of every industry report and the industries it belongs to
Writes: nganh/index.html, nganh/en/index.html     section index grouped by industry (rewritten whole)
        index.html, en/index.html                 industry row under the "Ngành"/"Sectors" heading (inserted)
        each report page listed in sections.json  "same industry" box at the end of <main> (inserted)
Every inserted block sits between <!-- industry-index --> markers and is replaced on each run, so the
script is safe to re-run and repairs the pages after a vault copy-in. No page is moved; old links keep working.

Run from the repository root:  python3 tools/industry-index/build.py
"""
import json, os, re, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
R = json.load(open(os.path.join(HERE, 'sections.json'), encoding='utf-8'))
E = lambda s: html.escape(str(s), quote=True)
MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
B0, B1 = '<!-- industry-index -->', '<!-- /industry-index -->'

# Mirae pages: titles and summaries come live from their own page text, so the index never drifts from the pages.
_mm = os.path.join(ROOT, 'tools', 'mirae-coverage', 'meta.json')
if os.path.exists(_mm):
    _m = json.load(open(_mm, encoding='utf-8'))
    _pg = {p['slug']: p for p in _m['pages']}; _pg[_m['overview']['slug']] = _m['overview']
    for r in R['reports']:
        slug = r['path'].strip('/').split('/')[-1]
        if r.get('built_by') == 'tools/mirae-coverage' and slug in _pg:
            r['title'] = dict(_pg[slug]['title']); r['sum'] = dict(_pg[slug]['dek'])
            r['tickers'] = _pg[slug].get('tickers', [])

IND = {i['id']: i for i in R['industries']}
STANCE = {}
if os.path.exists(_mm):
    for r in R['reports']:
        slug = r['path'].strip('/').split('/')[-1]
        if r.get('built_by') == 'tools/mirae-coverage' and slug in _pg and _pg[slug].get('stance'):
            for i in r['industries']: STANCE[i] = _pg[slug]['stance']
ORDER = [i['id'] for i in R['industries']]

def fdate(s, L):
    d = datetime.date.fromisoformat(s)
    return f'{d.day:02d}/{d.month:02d}/{d.year}' if L == 'vi' else f'{d.day} {MON[d.month - 1]} {d.year}'

def page_file(r, L):
    return os.path.join(ROOT, r['path'], 'en' if (L == 'en' and r['en']) else '', 'index.html')

def href(from_dir, r, L, anchor=''):
    """Relative link from a page directory (repo-relative) to report r in language L (falls back to Vietnamese)."""
    target = r['path'] + ('en/' if L == 'en' and r['en'] else '')
    rel = os.path.relpath(os.path.join(ROOT, target), os.path.join(ROOT, from_dir))
    return (rel.replace(os.sep, '/') + '/' if rel != '.' else './') + anchor

def by_industry(iid):
    return sorted([r for r in R['reports'] if iid in r['industries']], key=lambda r: (r['date'], r['kind'] == 'mirae'), reverse=True)

KIND_SHORT = {'mirae': {'vi': 'Mirae Asset', 'en': 'Mirae Asset'}, 'quarter': {'vi': 'Số liệu quý', 'en': 'Quarterly data'},
              'outlook': {'vi': 'Triển vọng', 'en': 'Outlook'}, 'earnings': {'vi': 'KQKD', 'en': 'Earnings'}}
def row(from_dir, r, L, iid):
    other = [IND[i][L]['name'] for i in r['industries'] if i != iid and i in IND]
    meta = fdate(r['date'], L)
    if L == 'en' and not r['en']: meta += ' · in Vietnamese'
    if other: meta += (' · cũng thuộc ' if L == 'vi' else ' · also in ') + ', '.join(other)
    tk = f'<span class="tks">{E(" ".join(r["tickers"]))}</span>' if r.get('tickers') else ''
    return (f'<li><span class="kd k-{r["kind"]}">{E(KIND_SHORT[r["kind"]][L])}</span><div><a class="rt" href="{href(from_dir, r, L)}">{E(r["title"][L])}</a>'
            f'<p class="rs">{E(r["sum"][L])}</p><p class="rm">{E(meta)}{tk}</p></div></li>\n')

def card(from_dir, r, L, iid):
    kind = R['kinds'][r['kind']][L]
    other = [IND[i][L]['name'] for i in r['industries'] if i != iid]
    meta = fdate(r['date'], L)
    if L == 'en' and not r['en']: meta += ' · In Vietnamese'
    if other: meta += (' · cũng thuộc: ' if L == 'vi' else ' · also in: ') + ', '.join(other)
    if r.get('tickers'): meta += ' · ' + ' '.join(r['tickers'])
    return (f'<a class="card" href="{href(from_dir, r, L)}"><p class="label">{E(kind)}</p><h3>{E(r["title"][L])}</h3>'
            f'<p class="sum">{E(r["sum"][L])}</p><p class="meta">{E(meta)}</p></a>\n')

CSS = ('<style>.ind-nav{display:flex;flex-wrap:wrap;gap:6px 8px;margin:16px 0 4px}'
       '.ind-nav a{font-size:13.5px;font-weight:600;border:1px solid var(--border);border-radius:999px;padding:3px 12px;background:var(--surface-1)}'
       '.ind-nav a span{color:var(--text-muted);font-weight:400;margin-left:4px}'
       'h2.ind{font-size:22px;margin:44px 0 4px;scroll-margin-top:12px}h2.ind span{color:var(--text-muted);font-weight:400;font-size:16px;margin-left:6px}'
       'p.ind-about{color:var(--text-secondary);margin:0 0 14px;max-width:72ch}'
       '.same-ind{margin:40px 0 0;padding:14px 18px;border:1px solid var(--border);border-radius:12px;background:var(--surface-1);max-width:80ch}'
       '.same-ind h2{font-size:15px;margin:0 0 6px;letter-spacing:0}.same-ind ul{margin:4px 0;padding-left:18px}.same-ind li{font-size:14.5px;margin:5px 0}'
       '.same-ind .k{color:var(--text-muted);font-size:12.5px}'
       'ul.rl{list-style:none;padding:0;margin:8px 0 0;border:1px solid var(--border);border-radius:12px;background:var(--surface-1)}'
       'ul.rl li{display:grid;grid-template-columns:118px 1fr;gap:4px 14px;padding:13px 18px;margin:0;max-width:none;border-top:1px solid var(--grid)}ul.rl li:first-child{border-top:0}'
       'ul.rl .kd{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--text-muted);padding-top:3px}ul.rl .k-mirae{color:var(--series-1)}'
       'ul.rl .rt{font-weight:650;font-size:16.5px;line-height:1.35;color:var(--text-primary)}ul.rl .rt:hover{color:var(--series-1)}'
       'ul.rl .rs{margin:3px 0 0;color:var(--text-secondary);font-size:14.5px;line-height:1.5;max-width:80ch;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}'
       'ul.rl .rm{margin:4px 0 0;font-size:12.5px;color:var(--text-muted);max-width:none}ul.rl .tks{margin-left:8px;letter-spacing:.02em}'
       'p.ind-view{margin:-6px 0 10px;font-size:14px;color:var(--text-secondary);max-width:80ch}p.ind-view b{color:var(--text-primary)}'
       '@media (max-width:560px){ul.rl li{grid-template-columns:1fr;padding:12px 14px}ul.rl .kd{padding-top:0}}</style>')

def nav_chips(from_dir, L, index_href):
    out = '<nav class="ind-nav" aria-label="' + ('Ngành' if L == 'vi' else 'Industries') + '">'
    for iid in ORDER:
        out += f'<a href="{index_href}#{iid}">{E(IND[iid][L]["name"])}<span>{len(by_industry(iid))}</span></a>'
    return out + '</nav>'

UNSORTED = {'vi': {'name': 'Chưa phân loại', 'about': 'Báo cáo mới chưa có trong sổ đăng ký ngành (tools/industry-index/sections.json). Thêm một dòng ở đó để xếp vào đúng ngành.'},
            'en': {'name': 'Not yet sorted', 'about': 'New reports not yet in the industry registry (tools/industry-index/sections.json). Add a row there to place them.'}}
def unknown_reports(L):
    """Cards on the current index (or, for English, the homepage's Sectors list) that the registry does not know."""
    known = {r['path'] for r in R['reports']}
    srcs = ([('nganh/index.html', 'nganh/'), ('index.html', '')] if L == 'vi' else [('nganh/en/index.html', 'nganh/en/'), ('en/index.html', 'en/')])
    out, seen = [], set()
    for f, d in srcs:
        fp = os.path.join(ROOT, f)
        if not os.path.exists(fp): continue
        h = open(fp, encoding='utf-8').read()
        if f in ('index.html', 'en/index.html'):   # homepages: only the sector section
            m = re.search(r'id="nganh".*?(?=<h2 class="section"|</main>)', h, re.S); h = m.group(0) if m else ''
        cards = re.finditer(r'<a class="card" href="([^"]+)">(?:<!--[^>]*-->)?<p class="label">[^<]*</p><h3>([^<]*)</h3><p class="sum">([^<]*)</p><p class="meta">([^<]*)</p>', h)
        rows = re.finditer(r'<a class="rt" href="([^"]+)">([^<]*)</a><p class="rs">([^<]*)</p><p class="rm">([^<]*)', h)
        for m in list(cards) + list(rows):
            tgt = os.path.normpath(os.path.join(d, m.group(1))).replace(os.sep, '/')
            path = re.sub(r'/?en$', '', tgt).rstrip('/') + '/'
            if path in known or path in seen or not path.startswith(('nganh/', 'ket-qua-kinh-doanh/')): continue
            seen.add(path)
            dm = re.search(r'(\d{2})/(\d{2})/(\d{4})', m.group(4)) or re.search(r'(\d{1,2}) (\w{3}) (\d{4})', m.group(4))
            date = '2000-01-01'
            if dm and '/' in dm.group(0): date = f'{dm.group(3)}-{dm.group(2)}-{dm.group(1)}'
            elif dm: date = f'{dm.group(3)}-{MON.index(dm.group(2)) + 1:02d}-{int(dm.group(1)):02d}'
            t, su = html.unescape(m.group(2)), html.unescape(m.group(3))
            out.append({'path': path, 'en': os.path.exists(os.path.join(ROOT, path, 'en', 'index.html')), 'date': date, 'kind': 'quarter',
                        'industries': ['_unsorted'], 'title': {'vi': t, 'en': t}, 'sum': {'vi': su, 'en': su}})
            print(f'  WARNING: {path} is on the {L} index but not in sections.json; kept under "{UNSORTED[L]["name"]}"')
    return out

def build_index(L):
    d = 'nganh/' if L == 'vi' else 'nganh/en/'
    f = os.path.join(ROOT, d, 'index.html')
    if L == 'vi':
        h = open(f, encoding='utf-8').read()
    else:  # English chrome: built from the Vietnamese index's head and the English homepage's header and footer
        vi = open(os.path.join(ROOT, 'nganh', 'index.html'), encoding='utf-8').read()
        en_home = open(os.path.join(ROOT, 'en', 'index.html'), encoding='utf-8').read()
        head = re.search(r'<head>.*?</head>', vi, re.S).group(0).replace('../assets/', '../../assets/')
        top = re.search(r'<header class="topbar">.*?</header>', en_home, re.S).group(0)
        top = re.sub(r'href="\.\./', 'href="../../', top).replace('href="../../" hreflang="vi"', 'href="../" hreflang="vi"')
        top = top.replace('<a href="../../en/#nganh">', '<a href="../../en/#nganh" aria-current="page">')
        foot = re.search(r'<footer class="foot">.*?</footer>', en_home, re.S).group(0).replace('href="../en/"', 'href="../../en/"')
        h = f'<!doctype html>\n<html lang="en">{head}\n<body>{top}\n<main class="wrap">\n</main>\n{foot}\n</body></html>\n'
    unk = sorted(unknown_reports(L), key=lambda r: r['date'], reverse=True)
    n = len(R['reports']) + len(unk)
    last = max(r['date'] for r in R['reports'])
    if L == 'vi':
        title, intro = 'Ngành', ('Báo cáo theo ngành, gồm cả ngân hàng, sắp xếp theo ngành. Mỗi ngành gồm số liệu quý gần nhất, triển vọng của các công ty nghiên cứu, '
                                 'và phần đọc nghiên cứu Mirae Asset theo ba khung: mốc theo dõi, động lực và bộ đệm. Một báo cáo bao nhiều ngành sẽ có mặt ở mỗi ngành đó.')
        h = re.sub(r'<title>[^<]*</title>', '<title>Ngành · Nghiên cứu cổ phiếu Việt Nam</title>', h)
        h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Báo cáo ngành sắp xếp theo ngành: số liệu quý, triển vọng và nghiên cứu Mirae Asset (mốc theo dõi, động lực, bộ đệm).">', h)
        h = h.replace('href="../en/#nganh" hreflang="en"', 'href="en/" hreflang="en"')
        footn = f'<p>{n} bài · {len(ORDER)} ngành · cập nhật {fdate(last, L)}</p>'
    else:
        title, intro = 'Sectors', ('Sector reports, banks included, grouped by industry. Each industry holds the latest quarterly data, the research houses\' outlook, '
                                   'and the reading of Mirae Asset research in three frames: milestones, drivers and cushion. A report that covers several industries appears under each.')
        h = re.sub(r'<title>[^<]*</title>', '<title>Sectors · Vietnam Equity Research</title>', h)
        h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Sector reports grouped by industry: quarterly data, outlooks and Mirae Asset research (milestones, drivers, cushion).">', h)
        footn = f'<p>{n} reports · {len(ORDER)} industries · updated {fdate(last, L)}</p>'
    kicker = 'Nghiên cứu cổ phiếu Việt Nam' if L == 'vi' else 'Vietnam Equity Research'
    body = f'<p class="kicker">{kicker}</p><h1>{title}</h1><p class="intro">{E(intro)}</p>' + nav_chips(d, L, '')
    for iid in ORDER:
        rs = by_industry(iid)
        st = STANCE.get(iid)
        view = (f'<p class="ind-view"><b>Mirae Asset:</b> {E(st[L])}</p>' if st else '')
        body += (f'<h2 class="ind" id="{iid}">{E(IND[iid][L]["name"])}<span>{len(rs)}</span></h2><p class="ind-about">{E(IND[iid][L]["about"])}</p>{view}'
                 '<ul class="rl">\n' + ''.join(row(d, r, L, iid) for r in rs) + '</ul>\n')
    if unk:
        body += (f'<h2 class="ind" id="chua-phan-loai">{E(UNSORTED[L]["name"])}<span>{len(unk)}</span></h2><p class="ind-about">{E(UNSORTED[L]["about"])}</p>'
                 '<ul class="rl">\n' + ''.join(row(d, r, L, '_unsorted') for r in unk) + '</ul>\n')
    h = re.sub(r'<main class="wrap">.*?</main>', lambda m: f'<main class="wrap">\n{body}</main>', h, flags=re.S)
    h = re.sub(r'(<footer class="foot"><div class="inner"><p>.*?</p>)(<p>[^<]*</p>)?(</div></footer>)', lambda m: m.group(1) + footn + m.group(3), h, flags=re.S)
    if CSS not in h: h = h.replace('</head>', CSS + '</head>', 1)
    os.makedirs(os.path.dirname(f), exist_ok=True)
    open(f, 'w', encoding='utf-8').write(h)

def strip_blocks(h):
    return re.sub(re.escape(B0) + r'.*?' + re.escape(B1) + r'\n?', '', h, flags=re.S)

def homepage(L):
    f = os.path.join(ROOT, 'index.html' if L == 'vi' else 'en/index.html')
    h = strip_blocks(open(f, encoding='utf-8').read())
    if L == 'vi':
        anchor = '<h2 class="section" id="nganh"><a href="nganh/">Ngành</a></h2>'
        chips = nav_chips('', L, 'nganh/')
    else:
        h = h.replace('<h2 class="section" id="nganh">Sectors</h2>', '<h2 class="section" id="nganh"><a href="../nganh/en/">Sectors</a></h2>')
        anchor = '<h2 class="section" id="nganh"><a href="../nganh/en/">Sectors</a></h2>'
        chips = nav_chips('en/', L, '../nganh/en/')
    if anchor not in h: print('  WARNING: homepage anchor not found in', f); return
    h = h.replace(anchor, anchor + B0 + chips + B1, 1)
    if CSS not in h: h = h.replace('</head>', CSS + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(h)

def same_industry(r, L):
    f = page_file(r, L)
    if not os.path.exists(f) or (L == 'en' and not r['en']): return
    d = r['path'] + ('en/' if L == 'en' else '')
    h = strip_blocks(open(f, encoding='utf-8').read())
    idx = os.path.relpath(os.path.join(ROOT, 'nganh/' if L == 'vi' else 'nganh/en/'), os.path.join(ROOT, d)).replace(os.sep, '/') + '/'
    box = ''
    for iid in r['industries']:
        others = [o for o in by_industry(iid) if o is not r]
        name = IND[iid][L]['name']
        head = (f'Cùng ngành: <a href="{idx}#{iid}">{E(name)}</a>' if L == 'vi' else f'Same industry: <a href="{idx}#{iid}">{E(name)}</a>')
        items = ''.join(f'<li><a href="{href(d, o, L)}">{E(o["title"][L])}</a> <span class="k">· {E(R["kinds"][o["kind"]][L])} · {fdate(o["date"], L)}'
                        f'{" · In Vietnamese" if L == "en" and not o["en"] else ""}</span></li>' for o in others)
        box += f'<h2>{head}</h2>' + (f'<ul>{items}</ul>' if items else '')
    block = f'{B0}<aside class="same-ind">{box}</aside>{B1}'
    if '</main>' not in h: print('  WARNING: no </main> in', f); return
    h = h.replace('</main>', block + '\n</main>', 1)
    if CSS not in h: h = h.replace('</head>', CSS + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(h)

if __name__ == '__main__':
    for r in R['reports']:
        assert all(i in IND for i in r['industries']), r['path']
        assert os.path.exists(page_file(r, 'vi')), 'missing page: ' + r['path']
    build_index('vi'); build_index('en')
    homepage('vi'); homepage('en')
    for r in R['reports']:
        same_industry(r, 'vi'); same_industry(r, 'en')
    print('industry index:', len(R['reports']), 'reports in', len(ORDER), 'industries; /nganh/ and /nganh/en/ rebuilt, homepages and report pages linked')
