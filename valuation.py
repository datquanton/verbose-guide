# -*- coding: utf-8 -*-
"""Evaluate the STB Valuation sheet the way Excel will, from the workbook.

Every cell the sheet needs is either an input we can read or a per-share figure
model_read already derives, so the whole thing can be reproduced here - and it
has to be, because Excel is unavailable and the sheet's caches predate the
booked formulas.

The sheet blends two legs 50/50 into D74, which Model!AI1 reads, so D74 is the
price the model's own P/E and P/B rows are struck on:

  P/B leg          fair P/B = (ROE - g) / (r - g), applied to that year's BPS,
                   rounded to the nearest VND100.  Booked on FY28F.
  Residual income  RI(t) = EPS(t) - r x opening book value per share, the three
                   forecast years discounted to today, plus a Gordon terminal
                   on the FY28F residual, plus opening book value.
  D74              ROUNDUP of the weighted average, to the nearest VND100.

The RI leg discounts on DATEDIF(TODAY(), ...), so it drifts a little every day.
TODAY is a parameter here rather than a call to the clock, so a rerun is
reproducible; main() prints the date it used.
"""
import datetime
import math

from model_read import F, _m, sheet, MODEL

VAL = sheet(MODEL, 'Valuation')
BOOKED = datetime.date(2026, 8, 6)          # the date the deck was cut


def num(ref):
    v = VAL[ref][1]
    if v is None:
        raise ValueError('Valuation!%s has no value' % ref)
    return v


def serial(n):
    """Excel serial date -> date.  1900-based, with the 1900 leap-year fudge."""
    return datetime.date(1899, 12, 30) + datetime.timedelta(days=int(n))


def build(today=BOOKED):
    ps = lambda v: v * 1000 / F['shares']
    g, rf, beta, mrp = num('B7'), num('B10'), num('B11'), num('B12')
    r = rf + beta * mrp                                   # B9, cost of equity

    # --- P/B leg, on FY28F (Valuation!K6 = Model!AA314, K15 = Model!AA941)
    roe = F['roe'][2] / 100
    bps = ps(F['equity'][2])
    fair_pb = (roe - g) / (r - g)
    pb_leg = round(fair_pb * bps / 1000, 1) * 1000

    # --- residual income leg.  Opening book value per column is the prior
    # column's row 54, which the sheet builds as book value + EPS.
    open_bv = [ps(_m.v('W85')) + ps(_m.v('X153')),        # I54, into FY26F
               ps(_m.v('CT85')) + ps(F['npatmi'][0]),     # J54, into FY27F
               ps(F['equity'][0]) + ps(F['npatmi'][1])]   # K54, into FY28F
    eps = [ps(n) for n in F['npatmi']]
    ri = [e - r * b for e, b in zip(eps, open_bv)]
    yrs = [(serial(num(c + '47')) - today).days / 365 for c in 'JKL']
    df = [1 / (1 + r) ** t for t in yrs]
    pv_ri = sum(a * b for a, b in zip(ri, df))
    terminal = ri[2] * (1 + g) / (r - g) * df[0]          # B61 x B62
    ri_leg = round((ps(_m.v('CT85')) + terminal + pv_ri) / 100) * 100

    w_pb, w_ri = num('C71'), num('C73')
    fair = math.ceil((w_pb * pb_leg + w_ri * ri_leg) / 100) * 100
    return dict(coe=r, g=g, beta=beta, fair_pb=fair_pb, bps=bps, roe=roe,
                pb_leg=pb_leg, ri_leg=ri_leg, ri=ri, df=df, years=yrs,
                terminal=terminal, pv_ri=pv_ri, weights=(w_pb, w_ri),
                fair_value=fair, price=num('D75'),
                upside=fair / num('D75') - 1)


V = build()


if __name__ == '__main__':
    print('valued at %s, on the deck date\n' % BOOKED.isoformat())
    print('cost of equity   %.3f%%   = %.2f%% + %.2f x %.2f%%'
          % (V['coe'] * 100, num('B10') * 100, V['beta'], num('B12') * 100))
    print('terminal growth  %.2f%%' % (V['g'] * 100))
    print()
    print('P/B leg, FY28F')
    print('  sustainable ROE   %8.2f%%' % (V['roe'] * 100))
    print('  fair P/B          %8.3fx  = (ROE - g) / (CoE - g)' % V['fair_pb'])
    print('  BPS FY28F         %8s' % '{:,.0f}'.format(V['bps']))
    print('  fair value        %8s' % '{:,.0f}'.format(V['pb_leg']))
    print()
    print('Residual income leg')
    for lab, ri, t, d in zip(('FY26F', 'FY27F', 'FY28F'), V['ri'], V['years'], V['df']):
        print('  RI %s          %8s   %.3f yrs, DF %.4f'
              % (lab, '{:,.0f}'.format(ri), t, d))
    print('  PV of RI          %8s' % '{:,.0f}'.format(V['pv_ri']))
    print('  PV of terminal    %8s' % '{:,.0f}'.format(V['terminal']))
    print('  fair value        %8s' % '{:,.0f}'.format(V['ri_leg']))
    print()
    print('weights %.0f%% / %.0f%%   ->  fair value %s   vs price %s, %+.1f%%'
          % (V['weights'][0] * 100, V['weights'][1] * 100,
             '{:,.0f}'.format(V['fair_value']), '{:,.0f}'.format(V['price']),
             V['upside'] * 100))


def display_cells(v=None):
    """The Valuation sheet's derived values, for writing back into the caches."""
    v = v or V
    df0 = v['df'][0]
    out = {'B1': v['fair_value'], 'B3': v['upside'], 'B9': v['coe'],
           'B58': v['pv_ri'], 'B61': v['terminal'] / df0, 'B62': df0,
           'B63': v['terminal'], 'B64': v['ri_leg'],
           'B71': v['pb_leg'], 'B73': v['ri_leg'],
           'D71': v['pb_leg'] * v['weights'][0], 'D73': v['ri_leg'] * v['weights'][1],
           'D74': v['fair_value'], 'D76': v['upside'],
           'K6': v['roe'], 'K14': v['fair_pb'], 'K15': v['bps'], 'K16': v['pb_leg']}
    # the P/B block's own columns, which read the model's per-share rows
    ps = lambda x: x * 1000 / F['shares']
    for col, i in (('I', 0), ('J', 1)):
        roe, bps = F['roe'][i] / 100, ps(F['equity'][i])
        pb = (roe - v['g']) / (v['coe'] - v['g'])
        out.update({col + '6': roe, col + '14': pb, col + '15': bps,
                    col + '16': round(pb * bps / 1000, 1) * 1000})
    for col, i in (('J', 0), ('K', 1), ('L', 2)):
        out[col + '55'] = v['ri'][i]
        out[col + '56'] = v['df'][i]
        out[col + '57'] = v['ri'][i] * v['df'][i]
        out[col + '53'] = ps(F['npatmi'][i])
    return out
