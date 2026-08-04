# -*- coding: utf-8 -*-
"""Figures for the FPT 2Q26 report.

Every series carries a direct value label, which is also the relief the palette
validator asks for on the aqua slot (contrast 2.74:1 against the surface).
Two-series charts get a legend; single-series ones are named by the title.
All figures are on the post-deconsolidation basis, so 1H25 is FPT's own
restated comparative (revenue 23,326, PBT 4,838), never the 32,683/6,166 that
was published before FPT Telecom moved to the equity method.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUT = '/home/user/verbose-guide/fig'
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'
SURFACE, INK, MUTED, GRID = '#fcfcfb', '#1a1a1a', '#5c5c5c', '#dcdcd8'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5,
                     'axes.edgecolor': GRID, 'text.color': INK,
                     'axes.labelcolor': MUTED, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'figure.facecolor': SURFACE,
                     'axes.facecolor': SURFACE, 'savefig.facecolor': SURFACE})


def frame(ax, ymax):
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.grid(axis='y', color=GRID, linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', length=0)
    ax.set_ylim(0, ymax)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: '{:,.0f}'.format(v)))


def save(fig, name):
    fig.tight_layout(pad=0.4)
    fig.savefig('%s%s.png' % (OUT, name), dpi=200)
    plt.close(fig)
    print('fig%s.png' % name)


def grouped(name, cats, a, b, la, lb, yoy, ymax, unit='VNDbn'):
    fig, ax = plt.subplots(figsize=(4.35, 2.5))
    x = range(len(cats))
    w = 0.36
    ax.bar([i - w / 2 - 0.01 for i in x], a, w, label=la, color=BLUE, zorder=3)
    ax.bar([i + w / 2 + 0.01 for i in x], b, w, label=lb, color=ORANGE, zorder=3)
    for i, (va, vb, g) in enumerate(zip(a, b, yoy)):
        ax.text(i - w / 2 - 0.01, va + ymax * 0.02, '{:,.0f}'.format(va),
                ha='center', fontsize=7.5, color=MUTED)
        ax.text(i + w / 2 + 0.01, vb + ymax * 0.02, '{:,.0f}'.format(vb),
                ha='center', fontsize=7.5, color=INK, fontweight='bold')
        ax.text(i, ymax * 0.93, g, ha='center', fontsize=8,
                color='#b34a1f' if g.startswith('-') else '#1f6b3f')
    ax.set_xticks(list(x)); ax.set_xticklabels(cats, fontsize=8)
    ax.set_ylabel(unit, fontsize=7.5)
    frame(ax, ymax)
    ax.legend(frameon=False, fontsize=8, loc='upper right', ncol=2,
              bbox_to_anchor=(1.0, 1.16))
    save(fig, name)


# Fig 1 - revenue by segment, on the restated basis
grouped('1', ['Global IT', 'Domestic IT', 'Education,\ninvestment & others'],
        [16668, 3458, 3198], [18902, 4236, 3131],
        '1H25 (restated)', '1H26', ['+13.4%', '+22.5%', '-2.1%'], 24000)

# Fig 2 - PBT by segment.  Technology PBT less domestic IT gives global IT.
grouped('2', ['Global IT', 'Domestic IT', 'Education,\ninvestment & others'],
        [2681, 154, 2003], [3006, 308, 2400],
        '1H25 (restated)', '1H26', ['+12.1%', '+100.5%', '+19.8%'], 3800)

# Fig 3 - AI and data analytics revenue, and its share of Technology
fig, ax = plt.subplots(figsize=(4.35, 2.5))
vals, shares = [1187, 1842], ['5.9% of\nTechnology', '8.0% of\nTechnology']
ax.bar(['1H25', '1H26'], vals, 0.42, color=AQUA, zorder=3)
for i, (v, s) in enumerate(zip(vals, shares)):
    ax.text(i, v + 60, '{:,.0f}'.format(v), ha='center', fontsize=9,
            fontweight='bold', color=INK)
    ax.text(i, v / 2, s, ha='center', va='center', fontsize=8, color='white')
# the empty column between the two bars is the only collision-free space here
ax.text(0.5, 700, '+55% YoY,\nagainst +15% for\nTechnology overall',
        ha='center', va='center', fontsize=8.5, color=MUTED, linespacing=1.5)
ax.set_ylabel('VNDbn', fontsize=7.5)
frame(ax, 2350)
save(fig, '3')

# Fig 4 - NPATMI, with the basis break marked
fig, ax = plt.subplots(figsize=(4.35, 2.5))
yrs = ['FY23', 'FY24', 'FY25', 'FY26F', 'FY27F', 'FY28F']
vals = [6465, 7857, 9464, 10944, 12674, 14774]
yoy = ['', '+21.5%', '+20.5%', '+15.6%', '+15.8%', '+16.6%']
cols = [BLUE] * 3 + [ORANGE] * 3
ax.set_xticks(range(len(yrs)))
ax.bar(yrs, vals, 0.55, color=cols, zorder=3)
for i, v in enumerate(vals):
    ax.text(i, v + 260, '{:,.0f}'.format(v), ha='center', fontsize=8,
            fontweight='bold', color=INK)
# growth reads under the year rather than inside the bar, which is too narrow
ax.set_xticklabels(['%s\n%s' % (y, g) if g else y for y, g in zip(yrs, yoy)],
                   fontsize=8)
ax.axvline(2.5, color=MUTED, linewidth=1, linestyle=(0, (3, 3)), zorder=2)
ax.text(2.62, 16100, 'forecast', fontsize=7.5, color=MUTED)
ax.set_ylabel('VNDbn', fontsize=7.5)
frame(ax, 17600)
save(fig, '4')
