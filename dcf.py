# -*- coding: utf-8 -*-
"""FPT DCF rebuilt from 30/06/2026. Sum of parts, which is the right structure
once FPT Telecom is an associate rather than a subsidiary:

    equity value = PV(core operations) + associates at carrying value + net cash

Core EBIT, revenue and the tax rate come from the FS-anchored P&L. Net cash,
the associate carrying value and the share count are filed at 30/06/2026.
Capex, D&A and working capital are ESTIMATED - the model's schedules for all
three still contain FPT Telecom and a Q2 filing has no cash flow statement.
"""
REV  = [57194.6, 65027.0, 74232.0]        # FY26F-28F, rebuilt model
EBIT = [8475.0, 9626.0, 11117.0]          # core operating profit, ex-associates ex-financial
REV25_EXFOX = 50607.0
TAX = 0.1555                              # 1H26 realised, ex-associates
NET_CASH = 9065.476 + 19906.104 - (16367.802 + 2080.611)   # filed 30/06/2026
ASSOC_BV = 9994.655                       # filed 30/06/2026, note 17
SHARES = 1.703507121                      # bn, note 24
PRICE = 62900.0
RF, BETA, ERP = 0.043, 1.0, 0.08966       # model C22/C23, ERP implied by C24
KE = RF + BETA * ERP
KD = 0.050                                # 1H26 actual 3.97%; model carries 11.5%
DEBT = 16367.802 + 2080.611


def wacc(kd=KD, ke=KE, mkt=True):
    e = PRICE * SHARES * 1000 if mkt else 39851.531          # market cap or filed parent equity
    w = e / (e + DEBT)
    return w * ke + (1 - w) * kd * (1 - TAX)


def fcff(capex_r, da_r, wc_r):
    out, prev = [], REV25_EXFOX
    for r, e in zip(REV, EBIT):
        out.append(e * (1 - TAX) + r * da_r - r * capex_r - wc_r * (r - prev))
        prev = r
    return out


def value(w, g, capex_r=0.050, da_r=0.040, wc_r=0.12):
    f = fcff(capex_r, da_r, wc_r)
    h2 = f[0] * 0.55                                          # 2H26 only - we value at 30/06/26
    pv = h2 / (1 + w) ** 0.25 + f[1] / (1 + w) + f[2] / (1 + w) ** 2
    tv = f[2] * (1 + g) / (w - g) / (1 + w) ** 2
    eq = pv + tv + ASSOC_BV + NET_CASH
    return eq, pv, tv, eq * 1e9 / (SHARES * 1e9)


W, G = wacc(), 0.015
f = fcff(0.050, 0.040, 0.12)
print('cost of equity %.2f%% | cost of debt %.1f%% (actual 3.97%%, model 11.5%%)' % (KE*100, KD*100))
print('WACC %.2f%% on market weights | %.2f%% on filed book equity' % (W*100, wacc(mkt=False)*100))
print('net cash %.0f (filed) | associates at carrying value %.0f | shares %.4fbn'
      % (NET_CASH, ASSOC_BV, SHARES))
print('\n%-26s %10s %10s %10s' % ('', 'FY26F', 'FY27F', 'FY28F'))
print('%-26s %10.0f %10.0f %10.0f' % ('revenue', *REV))
print('%-26s %10.0f %10.0f %10.0f' % ('core EBIT', *EBIT))
print('%-26s %10.0f %10.0f %10.0f' % ('NOPAT @ 15.55%', *[e*(1-TAX) for e in EBIT]))
print('%-26s %10.0f %10.0f %10.0f' % ('+ D&A @ 4.0% of sales', *[r*0.04 for r in REV]))
print('%-26s %10.0f %10.0f %10.0f' % ('- capex @ 5.0% of sales', *[r*0.05 for r in REV]))
print('%-26s %10.0f %10.0f %10.0f' % ('- change in WC @ 12%', *[f[i] and (REV[i]-([REV25_EXFOX]+REV)[i])*0.12 for i in range(3)]))
print('%-26s %10.0f %10.0f %10.0f' % ('= FCFF', *f))

eq, pv, tv, ps = value(W, G)
print('\nPV of 2H26-FY28F FCFF %10.0f' % pv)
print('PV of terminal value  %10.0f   (%.0f%% of enterprise value)' % (tv, tv/(pv+tv)*100))
print('+ associates          %10.0f' % ASSOC_BV)
print('+ net cash            %10.0f' % NET_CASH)
print('= equity value        %10.0f' % eq)
print('per share             %10.0f   vs price %.0f (%+.1f%%), vs published target 78,750 (%+.1f%%)'
      % (ps, PRICE, ps/PRICE*100-100, ps/78750*100-100))

print('\nsensitivity - value per share')
print('%-9s' % 'WACC\\g' + ''.join('%9.1f%%' % (g*100) for g in (0.005,0.010,0.015,0.020,0.025)))
for dw in (-0.01,-0.005,0,0.005,0.01):
    w = W+dw
    print('%8.2f%%' % (w*100) + ''.join('%10.0f' % value(w,g)[3] for g in (0.005,0.010,0.015,0.020,0.025)))
print('\nsensitivity to the capex assumption (WACC %.2f%%, g 1.5%%)' % (W*100))
for cx in (0.040,0.045,0.050,0.055,0.060):
    print('  capex %.1f%% of sales -> %6.0f per share' % (cx*100, value(W,G,capex_r=cx)[3]))
print('\nif the model\'s 11.5%% cost of debt is kept: WACC %.2f%% -> %.0f per share'
      % (wacc(kd=0.115)*100, value(wacc(kd=0.115),G)[3]))
