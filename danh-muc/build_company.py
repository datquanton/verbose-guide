#!/usr/bin/env python3
"""Builds company.js for the portfolio consultant: the per-company fact base.

Input : two JSON files as returned by FiinQuantX FundamentalAnalysis for the tickers in market.js,
        years covering the last 11+ quarters, quarters 1-4, type consolidated:
          get_ratios                                   -> ratios.json
          get_financial_statement(statement=incomestatement) -> income.json
Output: company.js -> window.PM_COMPANY = {...}

    python3 build_company.py ratios.json income.json > company.js

Bases, checked against the raw statements:
  rev, np, gp, pbt       single quarter, VND bn (rev = net sales; total operating income for banks;
                         operating sales for securities firms; net insurance sales for insurers; np = profit to parent)
  roe, gm, nim, cof ...  provider ratios, trailing twelve months
  pe, pb                 provider figure at each quarter (latest = latest price); null for banks
Nothing here is a forecast or an estimate.
"""
import json, sys

def get(d, *path):
    for p in path:
        if not isinstance(d, dict): return None
        d = d.get(p)
    return d

def find(o, leaf):
    """first numeric value whose key path ends with `leaf` (statement layouts differ by company type)"""
    if isinstance(o, dict):
        for k, v in o.items():
            if k == leaf and isinstance(v, (int, float)): return v
        for v in o.values():
            r = find(v, leaf)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, leaf)
            if r is not None: return r
    return None

def bn(x): return None if x is None else round(x / 1e9, 1)
def r(x, k=4): return None if x is None else round(x, k)

def main(ratios_path, income_path):
    Q = json.load(open(ratios_path, encoding='utf-8'))['data']['records']
    S = json.load(open(income_path, encoding='utf-8'))['data']['records']
    out = {}
    key = lambda x: (x['year'], x['quarter'])
    tickers = sorted({x['ticker'] for x in S})
    latest = max(key(x) for x in S)
    for t in tickers:
        st = sorted([x for x in S if x['ticker'] == t], key=key)
        rt = {key(x): x for x in Q if x['ticker'] == t}
        if not st: continue
        typ = st[0].get('company_type') or 'Company'
        c = {'type': typ, 'q': [], 'rev': [], 'np': [], 'gp': [], 'pbt': [], 'audited': []}
        for x in st:
            nf = x.get('normalized_fields') or {}
            c['q'].append('%dQ%02d' % (x['quarter'], x['year'] % 100))
            c['rev'].append(bn(nf.get('revenue_equivalent'))); c['np'].append(bn(nf.get('parent_net_profit')))
            c['gp'].append(bn(nf.get('gross_profit')) if typ == 'Company' else None)
            pbt = nf.get('profit_before_tax')
            if pbt is None: pbt = find(x.get('financial_statement'), 'total_net_accounting_profit_loss_before_tax')
            c['pbt'].append(bn(pbt))
        c['last'] = key(st[-1]) == latest
        fs = st[-1].get('financial_statement')
        if typ == 'Company':    # items outside core operations in the latest quarter, VND bn
            c['fin'] = bn(find(fs, 'financial_income')); c['oth'] = bn(find(fs, 'total_net_other_income_expenses'))
            ie = find(fs, 'in_which_interest_expenses'); c['int'] = bn(-ie) if ie is not None else None
        if typ == 'Bank':
            p = find(fs, 'provision_for_credit_losses'); pp = find(fs, 'net_operating_profit_before_allowance_for_credit_loss')
            c['prov'] = bn(-p) if p is not None else None; c['ppop'] = bn(pp)
            prev = [x for x in st if key(x) == (latest[0] - 1, latest[1])]
            if prev:
                p0 = find(prev[0].get('financial_statement'), 'provision_for_credit_losses'); c['prov0'] = bn(-p0) if p0 is not None else None
        # ratio history, aligned to c['q']
        def series(*path): return [r(get(rt.get(key(x), {}), 'ratios', *path)) for x in st]
        if typ == 'Bank':
            c['roe'] = series('5_profitability_component', 'net_income_after_tax_before_unusual_items_as_percentage_of_average_shareholders_equity')
            c['nim'] = series('5_profitability_component', 'nim'); c['cof'] = series('5_profitability_component', 'average_cost_of_financing_cof')
            c['npl'] = series('4_liquidity_and_assets_component', 'debt_category_3_5_gross_loan_to_customer')
            c['g2'] = [None if a is None or b is None else r(a - b) for a, b in zip(series('4_liquidity_and_assets_component', 'debt_category_2_5_gross_loan_to_customer'), c['npl'])]
            c['cov'] = series('2_asset_quality_component', 'loan_loss_reserves_np_ls'); c['casa'] = series('2_asset_quality_component', 'casa_ratio')
            c['cir'] = series('3_efficiency_component', 'cost_to_income_ratio'); c['credit'] = series('6_growth_component', 'credit_growth_yo_y')
            c['ldr'] = series('4_liquidity_and_assets_component', 'gross_loan_deposit_ldr')
        else:
            c['roe'] = series('4_profitability_ratio', 'roe'); c['gm'] = series('4_profitability_ratio', 'gross_profit_margin')
            c['de'] = series('3_solvency_ratio', 'debt_to_equity_ratio'); c['cover'] = series('3_solvency_ratio', 'ebit_interest_coverage')
            c['pe'] = [r(v, 2) for v in series('7_valuation_ratios', 'p_e')]; c['pb'] = [r(v, 2) for v in series('7_valuation_ratios', 'p_b')]
            if typ == 'Company':
                c['doh'] = [r(v, 0) for v in series('1_activity_ratio', 'days_of_inventory_on_hand_doh')]
                c['fcf'] = series('5_cash_flow_ratio', 'free_cash_flow_revenue')
            if typ == 'Securities':
                c['mle'] = series('1_activity_ratio', 'margin_lending_owner_s_equity'); c['mlg'] = series('6_growth', 'margin_lending_growth_yo_y')
        del c['audited']
        out[t] = c
    res = {'asof': '%dQ%02d' % (latest[1], latest[0] % 100), 'source': 'FiinQuantX', 't': out}
    sys.stdout.write('/* Generated by build_company.py from FiinQuantX financial statements and ratios; do not edit by hand. */\n')
    sys.stdout.write('window.PM_COMPANY = ' + json.dumps(res, ensure_ascii=False, separators=(',', ':')) + ';\n')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
