# -*- coding: utf-8 -*-
"""Charts for the STB + FPT mobile report.

Portrait slides, so every figure is tall.  Where two measures have different
scales they go in stacked panels (small multiples), never on a second y-axis.
Bilingual: each figure is rendered once per language.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'
NAVY, AMBER = '#01437C', '#F38120'          # the template's own two brand colours
INK, MUTED, GRID = '#1a1a1a', '#5c5c5c', '#dcdcd8'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 13,
                     'text.color': INK, 'axes.labelcolor': MUTED,
                     'xtick.color': MUTED, 'ytick.color': MUTED,
                     'figure.facecolor': 'white', 'axes.facecolor': 'white',
                     'savefig.facecolor': 'white'})
YRS = ['FY24', 'FY25', 'FY26F', 'FY27F', 'FY28F']

L = {  # en, vn
    'nii': ('Net interest income', 'Thu nhập lãi thuần'),
    'noii': ('Non-interest income', 'Thu nhập ngoài lãi'),
    'pbt': ('Profit before tax', 'Lợi nhuận trước thuế'),
    'rev': ('Revenue', 'Doanh thu'),
    'npat': ('NPATMI', 'LNST-CĐTS'),
    'pe': ('P/E at target price (x)', 'P/E theo giá mục tiêu (lần)'),
    'pb': ('P/B at target price (x)', 'P/B theo giá mục tiêu (lần)'),
    'bn': ('VNDbn', 'tỷ đồng'),
}


def tidy(ax, pct=False):
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.grid(axis='y', color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis='both', length=0)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: '{:,.0f}'.format(v)))


def bars(ax, vals, color, fmt='{:,.0f}', width=0.6, labels=YRS):
    ax.bar(labels, vals, width, color=color, zorder=3)
    hi = max(vals)
    for i, v in enumerate(vals):
        ax.text(i, v + hi * 0.025, fmt.format(v), ha='center', fontsize=12,
                fontweight='bold', color=INK)
    ax.set_ylim(0, hi * 1.20)


def grouped(ax, series, colors, names, fmt='{:,.0f}'):
    n = len(series)
    w = 0.78 / n
    hi = max(max(s) for s in series)
    for k, (s, c, nm) in enumerate(zip(series, colors, names)):
        off = (k - (n - 1) / 2) * w
        ax.bar([i + off for i in range(len(YRS))], s, w * 0.92, label=nm,
               color=c, zorder=3)
        for i, v in enumerate(s):
            ax.text(i + off, v + hi * 0.02, fmt.format(v), ha='center',
                    fontsize=9.5, color=INK, rotation=90 if n > 2 else 0,
                    va='bottom')
    ax.set_xticks(range(len(YRS)))
    ax.set_xticklabels(YRS)
    ax.set_ylim(0, hi * 1.28)
    ax.legend(frameon=False, fontsize=12, ncol=n, loc='upper center',
              bbox_to_anchor=(0.5, 1.13))


def save(fig, name):
    fig.tight_layout(pad=1.0)
    fig.savefig('/home/user/verbose-guide/m_%s.png' % name, dpi=170)
    plt.close(fig)


# ------------------------------------------------------------------ STB
STB = dict(nii=[24532, 26681, 26704, 29545, 34079],
           noii=[4145, 5376, 5950, 7382, 8779],
           pbt=[12720, 7628, 8143, 12293, 20064],
           pe=[15.8, 28.2, 26.5, 17.5, 10.7],
           pb=[3.1, 2.8, 2.5, 2.2, 1.8])
FPT = dict(rev=[62849, 70208, 57284, 66048, 76654],
           pbt=[11070, 13134, 13070, 15159, 17671],
           npat=[7857, 9464, 10944, 12674, 14774],
           pe=[18.0, 17.3, 13.7, 11.8, 10.1],
           pb=[4.5, 4.3, 3.5, 3.0, 2.5])

for li, lang in enumerate(('en', 'vn')):
    # STB income statement
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 7.6))
    grouped(a1, [STB['nii'], STB['noii']], [BLUE, AQUA],
            [L['nii'][li], L['noii'][li]])
    a1.set_ylabel(L['bn'][li], fontsize=11); tidy(a1)
    bars(a2, STB['pbt'], ORANGE)
    a2.set_ylabel(L['bn'][li], fontsize=11)
    a2.set_title(L['pbt'][li], fontsize=13, color=NAVY, fontweight='bold', pad=8)
    tidy(a2)
    save(fig, 'stb_is_' + lang)

    # FPT income statement
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 7.6))
    bars(a1, FPT['rev'], BLUE)
    a1.set_ylabel(L['bn'][li], fontsize=11)
    a1.set_title(L['rev'][li], fontsize=13, color=NAVY, fontweight='bold', pad=8)
    tidy(a1)
    grouped(a2, [FPT['pbt'], FPT['npat']], [ORANGE, AQUA],
            [L['pbt'][li], L['npat'][li]])
    a2.set_ylabel(L['bn'][li], fontsize=11); tidy(a2)
    save(fig, 'fpt_is_' + lang)

    # valuation: P/E over P/B, each on its own panel
    for tick, d in (('stb', STB), ('fpt', FPT)):
        fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 7.6))
        bars(a1, d['pe'], NAVY, '{:.1f}')
        a1.set_title(L['pe'][li], fontsize=13, color=NAVY, fontweight='bold', pad=8)
        tidy(a1)
        bars(a2, d['pb'], AMBER, '{:.1f}')
        a2.set_title(L['pb'][li], fontsize=13, color=NAVY, fontweight='bold', pad=8)
        tidy(a2)
        save(fig, '%s_val_%s' % (tick, lang))

print('charts written')
