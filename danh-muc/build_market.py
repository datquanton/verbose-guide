#!/usr/bin/env python3
"""Builds market.js for the portfolio desk from FiinQuantX daily closes.

Input : one or more JSON files as returned by FiinQuantX Fetch_Trading_Data
        (records of {ticker, timestamp, close}, adjusted daily closes, ~260 sessions).
Output: market.js  ->  window.PM_MARKET = {...}

    python3 build_market.py prices1.json prices2.json ... > market.js

Everything here is measured from prices; nothing is a forecast.
  vol    annualised volatility of daily log returns (x sqrt(252)), %
  d200   last close vs its 200-session average, %   (null if < 200 sessions)
  d50    last close vs its 50-session average, %
  r3m    return over the last 63 sessions, %
  rs3m   r3m minus the VN-Index's r3m, percentage points
  dd     largest peak-to-trough fall inside the window, %
  beta   slope of daily returns on VN-Index daily returns
  corr   pairwise correlation of daily log returns (needs >= 60 common sessions)
Valuation and liquidity (pe, pb, cap, adtv) are the FiinQuantX snapshot of the same day.
"""
import json, math, sys

SECTORS = {
    "bank": "VCB BID CTG TCB MBB VPB ACB HDB VIB TPB STB LPB SHB SSB EIB",
    "broker": "TCX VCK SSI VPX VIX HCM VCI VND LPS MBS SHS FTS BSI",
    "property": "VHM VIC VRE KSF NVL KDH DXG PDR NLG DIG CEO TAL TCH",
    "indpark": "BCM KBC IDC SIP SZC",
    "steel": "HPG HSG NKG",
    "retail": "MWG FRT DGW PNJ PET DMX",
    "tech": "FPT CMG",
    "consumer": "VNM MSN SAB",
    "energy": "GAS PLX PVS PVD BSR",
    "utilities": "POW REE",
    "materials": "GVR DGC DCM DPM",
    "transport": "VJC HVN GMD",
    "construction": "VGC CTD",
    "other": "BVH",
}
# ticker: (name, trailing P/E, P/B, market cap in thousand bn VND, 20-session average traded value in bn VND)
SNAP = {
 "VCB":("Vietcombank",10.79,1.77,449.5,260.2),"BID":("BIDV",7.04,1.26,247.7,127.8),"CTG":("VietinBank",5.75,1.19,244.7,277.8),
 "TCB":("Techcombank",8.11,1.24,232.3,548.8),"MBB":("MBBank",5.46,1.23,192.8,267.8),"VPB":("VPBank",7.09,1.18,221.0,414.3),
 "ACB":("ACB",7.34,1.14,118.1,260.7),"HDB":("HDBank",7.6,1.64,147.1,546.3),"VIB":("VIB",6.79,1.05,52.5,125.4),
 "TPB":("TPBank",4.89,0.86,41.3,245.3),"STB":("Sacombank",88,2.09,134.2,252.7),"LPB":("LPBank",8.96,2.32,108.3,526.8),
 "SHB":("SHB",3.74,0.65,58.2,438.4),"SSB":("SeABank",15.86,1.2,52.2,195.9),"EIB":("Eximbank",157.85,1.13,30.2,162.9),
 "TCX":("TCBS",15.17,1.99,94.4,103.9),"VCK":("VPS",15.53,2.09,67.0,55.9),"SSI":("SSI",13,1.55,60.6,437.1),
 "VPX":("VPBankS",11.36,1.21,44.1,13.3),"VIX":("VIX",16.1,1.02,33.6,540.5),"HCM":("HSC",21.69,1.81,31.5,145.0),
 "VCI":("Vietcap",15.73,1.34,22.6,181.6),"VND":("VNDIRECT",10.51,1.01,22.1,177.0),"LPS":("LPS",21.98,1.21,21.7,21.0),
 "MBS":("MBS",10.3,1.43,16.1,57.0),"SHS":("SHS",16.25,0.95,11.9,185.4),"FTS":("FPTS",18.31,1.65,7.4,19.5),
 "BSI":("BSC",16.35,1.32,7.7,20.2),
 "VHM":("Vinhomes",5.17,1.78,511.0,501.6),"VIC":("Vingroup",43.73,9.77,1886.2,527.3),"VRE":("Vincom Retail",7.47,1.09,55.2,79.7),
 "KSF":("Sunshine Group",5.2,2.86,61.2,7.8),"NVL":("Novaland",4.1,0.58,33.3,228.3),"KDH":("Khang Điền",11.42,1.03,19.6,146.3),
 "DXG":("Bluemarq (DXG)",121.15,0.98,14.1,166.9),"PDR":("Phát Đạt",21.29,0.91,11.5,69.6),"NLG":("Nam Long",24.36,0.95,12.1,42.3),
 "DIG":("DIC Corp",13.14,0.85,8.6,63.4),"CEO":("CEO Group",38.62,1.13,7.1,98.5),"TAL":("Taseco Land",14.62,2.18,12.7,6.9),
 "TCH":("Hoàng Huy",17.01,1.11,13.5,111.1),
 "BCM":("Becamex",18.36,1.72,38.5,22.6),"KBC":("Kinh Bắc",14.41,0.97,25.2,91.7),"IDC":("IDICO",8.02,2.01,14.6,39.9),
 "SIP":("Sài Gòn VRG",8.64,2.33,12.1,5.2),"SZC":("Sonadezi Châu Đức",23.4,1.23,3.8,18.5),
 "HPG":("Hòa Phát",6.48,1.19,177.7,437.4),"HSG":("Hoa Sen",14.12,0.74,8.8,40.8),"NKG":("Nam Kim",25,0.78,6.1,80.3),
 "MWG":("Thế Giới Di Động",9.66,2.28,107.7,293.5),"FRT":("FPT Retail",19.35,5.02,26.3,93.3),"DGW":("Digiworld",9.25,2.63,8.8,61.3),
 "PNJ":("PNJ",4.53,0.58,7.7,162.5),"PET":("Petrosetco",27.62,3.02,7.8,37.7),"DMX":("Điện Máy Xanh",14.92,5.35,95.2,9.1),
 "FPT":("FPT",9.14,2.2,94.5,522.2),"CMG":("CMC",10.43,1.21,4.1,6.0),
 "VNM":("Vinamilk",9.83,3.25,112.0,131.6),"MSN":("Masan",11.4,2.38,104.0,350.3),"SAB":("Sabeco",11.8,2.64,54.8,21.0),
 "GAS":("PV Gas",11.9,2.4,175.4,68.0),"PLX":("Petrolimex",11.09,1.55,43.3,88.3),"PVS":("PTSC",8.4,1.12,17.6,72.6),
 "PVD":("PV Drilling",16.76,0.88,15.2,116.2),"BSR":("Bình Sơn",4.54,1.52,126.9,222.2),
 "POW":("PV Power",5.55,0.93,40.0,115.4),"REE":("REE",11.29,1.38,31.1,26.1),
 "GVR":("Cao su Việt Nam",13.74,1.83,116.0,49.9),"DGC":("Đức Giang",6.7,0.95,12.4,11.4),"DCM":("Đạm Cà Mau",5.89,1.35,16.0,70.9),
 "DPM":("Đạm Phú Mỹ",8.43,1.17,13.3,40.4),
 "VJC":("Vietjet",48.64,4.04,107.2,204.7),"HVN":("Vietnam Airlines",17,7.4,69.2,18.7),"GMD":("Gemadept",13.15,2.52,35.7,185.6),
 "VGC":("Viglacera",10.04,2.03,18.0,30.8),"CTD":("Coteccons",10.64,0.85,8.5,50.4),"BVH":("Bảo Việt",14.08,1.82,47.7,57.4),
}
SNAP_DATE = "2026-11-13"
INDEX = "VNINDEX"

def load(paths):
    px = {}
    for p in paths:
        d = json.load(open(p, encoding="utf-8"))
        for r in d["data"]["records"]:
            c = r.get("close")
            if c is None or c <= 0: continue
            px.setdefault(r["ticker"], {})[r["timestamp"][:10]] = float(c)
    return px

def rets(series):
    days = sorted(series)
    return {days[i]: math.log(series[days[i]] / series[days[i-1]]) for i in range(1, len(days))}

def corr(a, b):
    k = [d for d in a if d in b]
    n = len(k)
    if n < 60: return None, n
    xa = [a[d] for d in k]; xb = [b[d] for d in k]
    ma = sum(xa)/n; mb = sum(xb)/n
    va = sum((x-ma)**2 for x in xa); vb = sum((x-mb)**2 for x in xb)
    if va == 0 or vb == 0: return None, n
    cov = sum((x-ma)*(y-mb) for x, y in zip(xa, xb))
    return cov / math.sqrt(va*vb), n

def beta(a, m):
    k = [d for d in a if d in m]
    n = len(k)
    if n < 60: return None
    xa = [a[d] for d in k]; xm = [m[d] for d in k]
    ma = sum(xa)/n; mm = sum(xm)/n
    vm = sum((x-mm)**2 for x in xm)
    return sum((x-ma)*(y-mm) for x, y in zip(xa, xm)) / vm if vm else None

def stats(series, idx_r3m):
    days = sorted(series); v = [series[d] for d in days]; n = len(v)
    r = [math.log(v[i]/v[i-1]) for i in range(1, n)]
    m = sum(r)/len(r)
    vol = math.sqrt(sum((x-m)**2 for x in r)/(len(r)-1)) * math.sqrt(252) * 100
    last = v[-1]
    d200 = (last / (sum(v[-200:])/200) - 1) * 100 if n >= 200 else None
    d50 = (last / (sum(v[-50:])/50) - 1) * 100 if n >= 50 else None
    r3m = (last / v[-64] - 1) * 100 if n >= 64 else None
    peak = v[0]; dd = 0.0
    for x in v:
        peak = max(peak, x); dd = min(dd, x/peak - 1)
    rnd = lambda x, k=1: None if x is None else round(x, k)
    return {"n": n, "px": last, "asof": days[-1], "vol": rnd(vol), "d200": rnd(d200), "d50": rnd(d50),
            "r3m": rnd(r3m), "rs3m": rnd(None if r3m is None or idx_r3m is None else r3m - idx_r3m), "dd": rnd(dd*100)}

def main(paths):
    px = load(paths)
    sector_of = {t: s for s, ts in SECTORS.items() for t in ts.split()}
    idx = stats(px[INDEX], None)
    idx_r = rets(px[INDEX])
    tickers = [t for s in SECTORS.values() for t in s.split() if t in px and len(px[t]) >= 30]
    R = {t: rets(px[t]) for t in tickers}
    T = {}
    for t in tickers:
        s = stats(px[t], idx["r3m"])
        b = beta(R[t], idx_r)
        nm, pe, pb, cap, adtv = SNAP[t]
        T[t] = {"name": nm, "sec": sector_of[t], **s, "beta": None if b is None else round(b, 2),
                "pe": pe, "pb": pb, "cap": cap, "adtv": adtv}
    # lower triangle, correlation x100, null when not enough common history
    tri = []; pairs = {}
    for i, a in enumerate(tickers):
        for j in range(i):
            c, n = corr(R[a], R[tickers[j]])
            tri.append(None if c is None else int(round(c*100)))
            if c is not None:
                key = tuple(sorted((sector_of[a], sector_of[tickers[j]])))
                pairs.setdefault(key, []).append(c)
    secs = list(SECTORS)
    seccorr = {}
    for (a, b), v in pairs.items():
        seccorr[a + "|" + b] = round(sum(v)/len(v), 2)
    allc = [c for v in pairs.values() for c in v]
    out = {"asof": idx["asof"], "snap": SNAP_DATE, "sessions": idx["n"],
           "index": {k: idx[k] for k in ("px", "vol", "d200", "d50", "r3m", "dd")},
           "order": tickers, "tri": tri, "t": T, "sectors": secs, "seccorr": seccorr,
           "avgcorr": round(sum(allc)/len(allc), 2)}
    sys.stdout.write("/* Generated by build_market.py from FiinQuantX daily closes; do not edit by hand. */\n")
    sys.stdout.write("window.PM_MARKET = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n")

if __name__ == "__main__":
    main(sys.argv[1:])
