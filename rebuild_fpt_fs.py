# -*- coding: utf-8 -*-
"""Re-derive the FPT forecast lines from FPT's own 1H26 consolidated FS
(filed 21/07/2026). Prints the target values; does not write anything."""

# ---------------- 1H26 as filed, VNDbn ----------------
REV, COGS, GP      = 26268.500667974, 17744.981597072, 8523.519070902
SELL, GA           = 2151.390001298, 2492.872991324
FIN_INC, FIN_EXP   = 998.565958123, 667.663663135
DEP_INT, FX_G, DIV, OTH_I = 813.221646731, 149.738087442, 33.323977500, 2.282246450
INT_EXP, FX_L, PROV, OTH_E = 392.043947290, 209.914260301, 65.373872124, 0.331583420
ASSOC              = 1423.398496350
OTHER_INC, OTHER_EXP = 89.876711878, 9.113487844
PBT, TAX, MI       = 5714.320093652, 723.293696986 - 56.169558430, -7.829668431
NPATMI             = 5055.025623527

# interest-bearing balances, ex-FPT Telecom (FOX deconsolidated 01/01/2026)
FOX_DEP_25, FOX_CASH_25 = 12378.501219537, 713.425316747
BAL_25 = (29630.986737440 - FOX_DEP_25) + (10522.105729992 - FOX_CASH_25)   # deposits + cash
BAL_26H = 19406.056344517 + 9065.475533200
FY25_NPATMI = 9464.16
REV_F = [57194.606680, 65945.020200, 76536.739860]        # model Revenue!J2:L2
TARGET = [10848., 12549., 14608.]                          # 2H26 at +15% YoY, then the carried path

print('--- 1H26 ratios, as filed')
print('  COGS / revenue          %.3f%%' % (COGS / REV * 100))
print('  gross margin            %.3f%%' % (GP / REV * 100))
print('  selling / revenue       %.3f%%' % (SELL / REV * 100))
print('  admin / revenue         %.3f%%' % (GA / REV * 100))
print('  total opex / revenue    %.3f%%' % ((SELL + GA) / REV * 100))
print('  effective tax rate      %.2f%% of PBT | %.2f%% of the block ex-associates'
      % (TAX / PBT * 100, TAX / (PBT - ASSOC) * 100))
print('  minority interest       %+.1f  (essentially nil post-deconsolidation)' % MI)
print('  check PBT-tax-MI = NPATMI: %.1f vs %.1f' % (PBT - TAX - MI, NPATMI))

print('\n--- financial income, from Note 27/28')
print('  deposit interest %7.1f | FX gain %6.1f | dividends %5.1f | other %4.1f  = %7.1f'
      % (DEP_INT, FX_G, DIV, OTH_I, FIN_INC))
print('  interest expense %7.1f | FX loss %6.1f | provisions %4.1f | other %4.1f  = %7.1f'
      % (INT_EXP, FX_L, PROV, OTH_E, FIN_EXP))
print('  net financial income %.1f in the half' % (FIN_INC - FIN_EXP))
YIELD = DEP_INT * 2 / ((BAL_25 + BAL_26H) / 2)
GROWTH = (BAL_26H / BAL_25) ** 2 - 1
print('  interest-bearing balance ex-FOX: %.0f (31/12/25) -> %.0f (30/06/26)' % (BAL_25, BAL_26H))
print('  realised deposit yield %.2f%% | balance growing %.1f%% p.a.' % (YIELD * 100, GROWTH * 100))

# project the deposit book and its interest, holding the realised yield flat
bal = [BAL_26H * (BAL_26H / BAL_25)]                       # 31/12/2026
for _ in range(2):
    bal.append(bal[-1] * (1 + GROWTH))
dep = [DEP_INT + (BAL_26H + bal[0]) / 2 * YIELD / 2,       # 1H actual + 2H on the average balance
       (bal[0] + bal[1]) / 2 * YIELD,
       (bal[1] + bal[2]) / 2 * YIELD]
# FX and investment provisions are not forecastable: 1H26 actuals stand, nil assumed thereafter
inc = [dep[0] + FX_G + DIV * 2 + OTH_I * 2, dep[1] + DIV * 2.16 + 5, dep[2] + DIV * 2.33 + 5]
exp = [INT_EXP * 2 + FX_L + PROV + OTH_E * 2, INT_EXP * 2.06 + 50, INT_EXP * 2.12 + 50]
netfin = [i - e for i, e in zip(inc, exp)]
other = [170., 195., 225.]
assoc = [ASSOC * 2, ASSOC * 2 * 1.14, ASSOC * 2 * 1.14 ** 2]
ETR = TAX / (PBT - ASSOC)

print('\n%-30s %9s %9s %9s' % ('', 'FY26F', 'FY27F', 'FY28F'))
row = lambda l, xs, f='%9.0f': print(('%-30s ' % l) + ' '.join(f % x for x in xs))
row('year-end deposit balance', bal)
row('deposit interest income', dep)
row('financial income', inc)
row('financial expense', exp)
row('= net financial income', netfin)
row('  (model carried)', [558., 1004., 1029.])
row('associate income', assoc)
row('  (model carried)', [1850., 2109., 2404.])

# solve the operating block that lands each year on target
gp = [r * GP / REV for r in REV_F]
pbt = [(t - a * ETR) / (1 - ETR) for t, a in zip(TARGET, assoc)]
core = [p - nf - o - a for p, nf, o, a in zip(pbt, netfin, other, assoc)]
opex = [g - c for g, c in zip(gp, core)]
sell_sh = SELL / (SELL + GA)
sell = [o * sell_sh for o in opex]
admin = [o - s for o, s in zip(opex, sell)]
row('gross profit @ 1H26 margin', gp)
row('required operating expense', opex)
row('  as %% of revenue', [o / r * 100 for o, r in zip(opex, REV_F)], '%8.2f%%')
row('  selling %% of revenue', [s / r * 100 for s, r in zip(sell, REV_F)], '%8.3f%%')
row('  admin %% of revenue', [a / r * 100 for a, r in zip(admin, REV_F)], '%8.3f%%')
row('PBT', pbt)
row('tax @ %.2f%% ex-associates' % (ETR * 100), [(p - a) * ETR for p, a in zip(pbt, assoc)])
npat = [p - (p - a) * ETR for p, a in zip(pbt, assoc)]
row('NPATMI (MI nil)', npat)
prev = FY25_NPATMI
for y, v in zip(('FY26F', 'FY27F', 'FY28F'), npat):
    print('   %s growth %+.1f%%' % (y, v / prev * 100 - 100)); prev = v

print('\nCELLS TO WRITE')
print('  PL!Q11:S11  COGS            =Q9*%.3f%%' % (COGS / REV * 100))
print('  PL!Q19:S19  selling/sales    %s' % ['%.4f%%' % (s / r * 100) for s, r in zip(sell, REV_F)])
print('  PL!Q20:S20  admin           =Q9*%s' % ['%.4f%%' % (a / r * 100) for a, r in zip(admin, REV_F)])
print('  PL!Q32:S32  fin income       %s' % ['%.0f' % i for i in inc])
print('  PL!Q34:S34  fin expense      %s' % ['%.0f' % e for e in exp])
print('  PL!Q42:S42 / Q43:S43 other   net %s' % ['%.0f' % o for o in other])
print('  Scenarios!H45:J45 associates %s' % ['%.6f' % (a / r) for a, r in zip(assoc, REV_F)])
print('  PL!Q50:S50  tax             =(Q47-Q45)*%.2f%%' % (ETR * 100))
print('  PL!Q54:S54  minority interest 0')
