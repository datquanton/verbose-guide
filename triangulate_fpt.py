# -*- coding: utf-8 -*-
"""Triangulate FY26F FPT NPATMI four independent ways and stress the drivers.
Every input is either a reported figure or arithmetic on reported figures."""

# ---- reported (sources in INTERNAL_Sources_and_Assumptions_Aug26.xlsx)
FY25R_NPATMI  = 9464.16                      # basis-invariant under the equity method
Q1, Q2        = 2487., 2568.                 # 1H26 NPATMI, +14.4% / +14.0% YoY
G1, G2        = 0.144, 0.140
PBT_1H26      = 5714.                        # +18.1% YoY
PLAN_PBT      = 11629.                       # FY26 plan
FOX_1H26      = 1877.230816811               # FOX NPATMI 1H26
STAKE         = 0.4566
ETR, MI       = 0.12, 0.0149064              # 1H26-implied tax rate; model MI
A26           = 1850.                        # associate line carried in FY26F

# segment revenue: 1H26 actual (+YoY) and the FY26F model line, VNDbn
SEG = {                        # name          1H26     YoY      FY25R    FY26F   PBT margin
    'Global IT':              (18902., 0.134, 35382., 40572., None),
    'Domestic IT':            ( 4236., 0.225,  9093., 10184., 0.073),
    'Education, inv. & other':( 3131., -.021,  6132.,  6439., None),
}
TECH_PBT_1H, TECH_REV_1H = 3314., 23138.     # +16.9% YoY
EDU_PBT_1H = 2400.                           # includes the associate line

h1 = Q1 + Q2
h1_25 = Q1 / (1 + G1) + Q2 / (1 + G2)
h2_25 = FY25R_NPATMI - h1_25
share = h1_25 / FY25R_NPATMI
assoc_1h = FOX_1H26 * STAKE
CARRIED = 10848.

npatmi = lambda pbt, a: (pbt - (pbt - a) * ETR) * (1 - MI)
print('1H26 NPATMI %.0f (+%.1f%%) | 1H25R %.0f = %.1f%% of FY25R | 2H25R %.0f'
      % (h1, h1 / h1_25 * 100 - 100, h1_25, share * 100, h2_25))
print('1H26 PBT %.0f, of which associates %.0f -> operating %.0f' % (PBT_1H26, assoc_1h, PBT_1H26 - assoc_1h))
print()

routes = []
# 1 -- seasonality applied to reported NPATMI
routes.append(('1. NPATMI seasonality (1H share = FY25R 46.8%)', h1 / share))
# 2 -- seasonality applied to reported PBT, then the corrected tax/MI bridge
pbt2 = PBT_1H26 / share
routes.append(('2. PBT seasonality -> tax/MI bridge  (PBT %.0f)' % pbt2, npatmi(pbt2, A26)))
# 3 -- segment revenue x 1H26 realised margins
tech_m = TECH_PBT_1H / TECH_REV_1H
edu_m = (EDU_PBT_1H - assoc_1h) / SEG['Education, inv. & other'][0]     # strip the associate line out
tech_rev26 = SEG['Global IT'][3] + SEG['Domestic IT'][3]
op26 = tech_rev26 * tech_m + SEG['Education, inv. & other'][3] * edu_m
routes.append(('3. Segment revenue x 1H26 margins   (oper PBT %.0f)' % op26, npatmi(op26 + A26, A26)))
# 4 -- the model's own operating block + FOX-only associates
OP_MODEL = 9757.4739520375151 + 557.77599486055442 + 96.842056136005169
routes.append(('4. Model operating block + FOX only (assoc %.0f)' % (assoc_1h * 2.07),
               npatmi(OP_MODEL + assoc_1h * 2.07, assoc_1h * 2.07)))

print('%-52s %8s %8s %8s' % ('route', 'FY26F', 'YoY', 'vs carried'))
for name, v in routes:
    print('%-52s %8.0f %7.1f%% %9.1f%%' % (name, v, v / FY25R_NPATMI * 100 - 100, v / CARRIED * 100 - 100))
vals = [v for _, v in routes]
print('%-52s %8.0f %7.1f%%' % ('CARRIED', CARRIED, CARRIED / FY25R_NPATMI * 100 - 100))
print('\nspread of the four routes: %.0f - %.0f (%.1f%% wide); carried sits %.1f%% above the midpoint'
      % (min(vals), max(vals), (max(vals) / min(vals) - 1) * 100,
         (CARRIED / ((min(vals) + max(vals)) / 2) - 1) * 100))

# ---- what 2H26 has to do, segment by segment
print('\n%-26s %9s %9s %9s %9s' % ('2H26 revenue required', '1H26 YoY', '2H25R', '2H26F', 'YoY needed'))
for n, (r1h, g, fy25, fy26, _) in SEG.items():
    h2 = fy26 - r1h
    print('%-26s %8.1f%% %9.0f %9.0f %8.1f%%  %s'
          % (n, g * 100, fy25 - r1h / (1 + g), h2, (h2 / (fy25 - r1h / (1 + g)) - 1) * 100,
             'stretch' if (h2 / (fy25 - r1h / (1 + g)) - 1) > g else 'conservative'))

# ---- stress the three drivers that are not settled by 1H26
print()
base = CARRIED
shocks = [
 ('Global IT holds +13.4% in 2H (no AI reaccel.)',
  -(SEG['Global IT'][2] - SEG['Global IT'][0] / 1.134) * (0.158 - 0.134) * tech_m),
 ('Education/others flat in 2H, not +12.7%',
  -(SEG['Education, inv. & other'][2] - SEG['Education, inv. & other'][0] / 0.979) * 0.127 * edu_m),
 ('Domestic IT keeps +22.5% in 2H, not +5.6%',
  +(SEG['Domestic IT'][2] - SEG['Domestic IT'][0] / 1.225) * (0.225 - 0.056) * SEG['Domestic IT'][4]),
 ('Tax rate 13% not 12% (incentives roll off)', -(base / (1 - MI) - A26) / (1 - ETR) * 0.01),
 ('Associates = FOX run-rate 1,714, no others', -(A26 - 1714.)),
]
print('%-46s %9s %9s' % ('driver not settled by 1H26', 'NPATMI', 'FY26F'))
for n, d in shocks:
    print('%-46s %+9.0f %9.0f  (%.1f%%)' % (n, d * (1 - MI), base + d * (1 - MI),
                                            (base + d * (1 - MI)) / FY25R_NPATMI * 100 - 100))
down = sum(d for n, d in shocks if d < 0) * (1 - MI)
up = sum(d for n, d in shocks if d > 0) * (1 - MI)
print('\nall downside together  %8.0f  (%.1f%%)' % (base + down, (base + down) / FY25R_NPATMI * 100 - 100))
print('all upside together    %8.0f  (%.1f%%)' % (base + up, (base + up) / FY25R_NPATMI * 100 - 100))
print('plan-completion check: 1H26 PBT is %.1f%% of the FY26 plan (seasonal norm %.1f%%) -> '
      'implies a %.1f%% full-year beat' % (PBT_1H26 / PLAN_PBT * 100, share * 100,
                                           (PBT_1H26 / share) / PLAN_PBT * 100 - 100))
