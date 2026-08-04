// FPT 2Q26 report, in the house layout of EN_FPT_Report_2Q26.docx (the 2Q25
// edition): rating block + FY table, earnings overview with a 1H/2Q P&L table,
// segment table, figure pairs, then forecast and valuation.
// Run: node build_fpt_report.js
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, BorderStyle, ShadingType, PageBreak, Header, Footer, PageNumber,
  VerticalAlign, ImageRun,
} = require('docx');

const OUT = '/home/user/verbose-guide/MASVN_FPT_2Q26_Results_Review_Aug2026.docx';
const W = 10093;                      // A4 portrait less 1.6cm side margins
const NAVY = '1F3864', GREY = '595959', RULE = 'BFBFBF', BAND = 'F2F2F2';
const UP = '1F6B3F', DOWN = 'B34A1F';
const FONT = 'Calibri';

const T = (t, o = {}) => new TextRun({ text: t, font: FONT, ...o });
const P = (t, o = {}) => new Paragraph({
  children: Array.isArray(t) ? t : [T(t, o.run || {})],
  spacing: { after: o.after === undefined ? 120 : o.after, line: o.line || 250 },
  alignment: o.align, ...(o.border ? { border: o.border } : {}),
});
const H1 = (t) => new Paragraph({
  children: [T(t, { size: 22, bold: true, color: 'FFFFFF' })],
  shading: { type: ShadingType.CLEAR, fill: NAVY, color: 'auto' },
  spacing: { before: 200, after: 120, line: 260 },
  indent: { left: 80, right: 80 },
});
const H2 = (t) => new Paragraph({
  children: [T(t, { size: 19, bold: true, color: NAVY })],
  spacing: { before: 160, after: 80, line: 250 },
});
const cell = (children, o = {}) => new TableCell({
  children, width: { size: o.w, type: WidthType.DXA },
  margins: { top: 40, bottom: 40, left: 90, right: 90 },
  verticalAlign: VerticalAlign.CENTER,
  ...(o.fill ? { shading: { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } } : {}),
  borders: o.borders,
});
const thin = (c) => ({
  top: { style: BorderStyle.SINGLE, size: 2, color: c },
  bottom: { style: BorderStyle.SINGLE, size: 2, color: c },
  left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
});
const none = { top: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  bottom: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' } };

// a data table: first row is the header, first column left-aligned
function grid(rows, firstW, opts = {}) {
  const n = rows[0].length;
  const rest = Math.floor((W - firstW) / (n - 1));
  const widths = [firstW, ...Array(n - 1).fill(rest)];
  widths[n - 1] += W - widths.reduce((a, b) => a + b, 0);
  return new Table({
    columnWidths: widths, width: { size: W, type: WidthType.DXA },
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      children: r.map((v, ci) => {
        const bold = ri === 0 || (opts.boldRows || []).includes(ri);
        let color = ri === 0 ? 'FFFFFF' : '000000';
        if (ri > 0 && ci > 0 && typeof v === 'string') {
          if (v.startsWith('+')) color = UP;
          else if (v.startsWith('-') && v.endsWith('%')) color = DOWN;
        }
        return cell([new Paragraph({
          children: [T(String(v), { size: 16, bold, color })],
          alignment: ci === 0 ? AlignmentType.LEFT : AlignmentType.RIGHT,
          spacing: { before: 20, after: 20, line: 220 },
        })], {
          w: widths[ci],
          fill: ri === 0 ? NAVY : (opts.band && ri % 2 === 0 ? BAND : undefined),
          borders: thin(ri === 0 ? NAVY : RULE),
        });
      }),
    })),
  });
}

// two figures side by side, each captioned above and sourced below
function figures(a, b) {
  const half = Math.floor(W / 2);
  const img = (f) => new Paragraph({
    children: [new ImageRun({
      type: 'png', data: fs.readFileSync('/home/user/verbose-guide/' + f),
      transformation: { width: 232, height: 133 },
    })], spacing: { after: 40 },
  });
  const col = (fig) => [
    new Paragraph({ children: [T(fig.title, { size: 16, bold: true, color: NAVY })],
      spacing: { after: 60, line: 220 } }),
    img(fig.file),
    new Paragraph({ children: [T(fig.source, { size: 13, italics: true, color: GREY })],
      spacing: { after: 0, line: 200 } }),
  ];
  return new Table({
    columnWidths: [half, W - half], width: { size: W, type: WidthType.DXA },
    rows: [new TableRow({
      children: [cell(col(a), { w: half, borders: none }),
        cell(col(b), { w: W - half, borders: none })],
    })],
  });
}

// ------------------------------------------------------------------ content
const children = [];

children.push(new Paragraph({
  children: [T('Equity Research  ·  Vietnam  ·  IT', { size: 15, bold: true, color: GREY, allCaps: true })],
  spacing: { after: 60 },
}));
children.push(new Paragraph({
  children: [T('FPT Corporation', { size: 34, bold: true, color: NAVY }),
    T('   (HOSE: FPT)', { size: 20, color: GREY })],
  spacing: { after: 40, line: 380 },
}));
children.push(new Paragraph({
  children: [T('2Q26 review: growth held, and the AI line started paying', { size: 22 })],
  spacing: { after: 40, line: 280 },
}));
children.push(P([T('5 August 2026  ·  Quan Ton, quan.td@miraeasset.com.vn',
  { size: 15, color: GREY })], {
  after: 160,
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 6 } },
}));

children.push(grid([
  ['Rating', 'Target price', 'Current price (04/08/26)', 'Expected return', 'Market cap'],
  ['BUY (Update)', 'VND87,950', 'VND71,700', '+22.7%', 'VND122,141bn'],
], 2400));
children.push(P('', { after: 140 }));

children.push(P([T('1H26 revenue rose 12.6% and PBT 18.1% on FPT’s own restated base, '
  + 'lifting the group PBT margin to 21.8% from 20.7%. We keep our FY26F NPATMI at VND10,944bn '
  + '(+15.6% YoY) and our DCF target price at VND87,950 (BUY, 23% upside). The quarter’s '
  + 'most useful datapoint is not the headline: AI and data analytics revenue grew 55% to '
  + 'VND1,842bn and both AI Factories turned profitable, which is the first hard evidence that '
  + 'AI is adding to FPT’s revenue faster than it is compressing the headcount-based '
  + 'pricing it threatens.', { size: 18 })], { after: 60 }));

children.push(H1('2Q26 and 1H26 earnings overview'));
children.push(P([T('All comparatives here are FPT’s restated 1H25 figures. FPT Telecom moved '
  + 'to the equity method from FY26, so the previously published 1H25 revenue of VND32,683bn and '
  + 'PBT of VND6,166bn are not comparable with the 1H26 print; the restated base is VND23,326bn '
  + 'and VND4,838bn.', { size: 17, italics: true, color: GREY })], { after: 100 }));

children.push(grid([
  ['Table 1. 1H26 P&L (VNDbn)', '1H26', '1H25R', 'YoY', '2Q26', '1Q26', 'QoQ'],
  ['Net revenue', '26,269', '23,326', '+12.6%', '13,789', '12,480', '+10.5%'],
  ['Profit before tax', '5,714', '4,838', '+18.1%', '2,910', '2,804', '+3.8%'],
  ['PBT margin', '21.8%', '20.7%', '+1.0%p', '21.1%', '22.5%', '-1.4%p'],
  ['NPATMI', '5,055', 'n.a.', 'n.a.', '2,568', '2,487', '+3.3%'],
  ['  o/w Technology revenue', '23,138', '20,126', '+15.0%', '', '', ''],
  ['  o/w Technology PBT', '3,314', '2,835', '+16.9%', '', '', ''],
  ['  o/w Education, investment & others revenue', '3,131', '3,198', '-2.1%', '', '', ''],
  ['  o/w Education, investment & others PBT', '2,400', '2,003', '+19.8%', '', '', ''],
  ['Associate income', '1,423', '1,011', '+40.8%', '', '', ''],
], 3900, { band: true, boldRows: [1, 2, 4] }));
children.push(P([T('Note: 1H25R is FPT’s restated comparative. 1Q26 revenue and PBT are '
  + 'derived as 1H26 less the 2Q26 print. FPT restated 1H25 revenue, PBT and PAT but we have no '
  + 'restated 1H25 NPATMI, so no YoY is shown on that line; the 2Q26 print alone was +14% YoY. '
  + 'Source: FPT, Mirae Asset Vietnam Research',
  { size: 13, italics: true, color: GREY })], { after: 140, line: 200 }));

children.push(P([
  T('Revenue growth was carried by the technology segment. ', { size: 18, bold: true }),
  T('Technology revenue reached VND23,138bn (+15.0% YoY), 88% of the group, on PBT of '
    + 'VND3,314bn (+16.9%). Within it, Global IT grew 13.4% to VND18,902bn and Domestic IT 22.5% '
    + 'to VND4,236bn — the fastest-growing line in the group, on national '
    + 'digital-transformation awards. Domestic IT’s PBT doubled to VND308bn, though its 7.3% '
    + 'margin still dilutes the segment blend. Education, investment and others fell 2.1% to '
    + 'VND3,131bn but lifted PBT 19.8% to VND2,400bn, contributing 42% of group PBT on a margin '
    + 'near 77%.', { size: 18 })], { after: 120 }));

children.push(figures(
  { title: 'Figure 1. 1H26 revenue by segment', file: 'fig1.png',
    source: 'Source: FPT, Mirae Asset Vietnam Research' },
  { title: 'Figure 2. 1H26 PBT by segment', file: 'fig2.png',
    source: 'Source: FPT, Mirae Asset Vietnam Research' }));
children.push(P('', { after: 140 }));

children.push(P([
  T('Associate income is now a material line. ', { size: 18, bold: true }),
  T('With FPT Telecom (45.66%) equity-accounted alongside FPT Retail (46.5%), Synnex FPT (48%) '
    + 'and FPT Online (49.5%), associate income reached VND1,423bn in 1H26, up 40.8% YoY. That '
    + 'is 25% of group PBT, against a line that was immaterial two years ago, and it is the '
    + 'single largest reason group PBT growth (+18.1%) outpaced revenue growth (+12.6%).',
    { size: 18 })], { after: 120 }));

children.push(new Paragraph({ children: [new PageBreak()] }));

children.push(H1('The AI question, answered in FPT’s own numbers'));
children.push(P([T('The bear case on FPT is that AI compresses per-hour billing faster than it '
  + 'expands demand. 1H26 is the first period with enough disclosure to test that, and it cuts '
  + 'the other way.', { size: 18 })], { after: 100 }));
children.push(P([
  T('AI and data analytics revenue reached VND1,842bn, +55% YoY against +15% for Technology as '
    + 'a whole, lifting its share of the segment to 8.0% from 5.9%. That single line contributed '
    + 'roughly a fifth of Technology’s growth; strip it out and the segment grew 12.5%. Both '
    + 'AI Factories — Vietnam and Japan — ran above 90% utilisation and turned '
    + 'profitable in 2Q26, about a year after launch, which is faster than we assumed. ',
    { size: 18 }),
  T('The caveat: 8% of one segment cannot yet offset pricing pressure on the other 92%, and the '
    + 'margin disclosure is not granular enough to see whether AI work is being priced at a '
    + 'premium or simply substituting for headcount. We treat this as directional evidence, not '
    + 'proof.', { size: 18, italics: true })], { after: 120 }));

children.push(figures(
  { title: 'Figure 3. AI & data analytics revenue', file: 'fig3.png',
    source: 'Source: FPT, Mirae Asset Vietnam Research' },
  { title: 'Figure 4. NPATMI and growth', file: 'fig4.png',
    source: 'Source: FPT, Mirae Asset Vietnam Research' }));
children.push(P('', { after: 140 }));

children.push(P([
  T('The order book supports a Global IT reacceleration. ', { size: 18, bold: true }),
  T('Signed contract value for Global IT reached VND26,338bn in 1H26, +32.3% YoY, including 14 '
    + 'deals above USD10mn. That is a book-to-bill of 1.39x against 1.07–1.22x through '
    + 'FY21–25 — the widest gap between orders and revenue in five years. On that basis '
    + 'we look for Global IT to grow 14.7% in FY26F and reaccelerate to 16.7% in FY27F and 17.7% '
    + 'in FY28F, from 13.4% delivered in 1H26. The US book is the exception, cut to +5.9% on '
    + 'price competition and tariff-related deal slippage.', { size: 18 })], { after: 120 }));

children.push(H1('Forecast and valuation'));
children.push(grid([
  ['Table 2. Forecast summary (VNDbn)', 'FY25', 'FY26F', 'FY27F', 'FY28F'],
  ['Revenue', '70,208', '57,284', '66,048', '76,654'],
  ['  % YoY', '+11.7%', 'n.m.*', '+15.3%', '+16.1%'],
  ['Operating profit', '11,079', '9,807', '11,044', '13,053'],
  ['Profit before tax', '13,134', '13,070', '15,159', '17,671'],
  ['Associate income', '658', '2,608', '2,999', '3,449'],
  ['NPATMI', '9,464', '10,944', '12,674', '14,774'],
  ['  % YoY', '+20.5%', '+15.6%', '+15.8%', '+16.6%'],
  ['EPS (VND)', '5,073', '6,424', '7,440', '8,673'],
  ['ROE (%)', '28.6', '27.6', '27.1', '26.5'],
  ['P/E at target price (x)', '17.3', '13.7', '11.8', '10.1'],
], 3900, { band: true, boldRows: [6, 7] }));
children.push(P([T('* FY26F revenue is not comparable with FY25 as reported: FPT Telecom is '
  + 'equity-accounted from FY26F. Against a restated FY25 revenue of VND50,607bn the change is '
  + '+13.2%. NPATMI is unaffected by the change of basis. P/E is struck on the target price of '
  + 'VND87,950. Source: Company data, Mirae Asset Vietnam Research',
  { size: 13, italics: true, color: GREY })], { after: 140, line: 200 }));

children.push(P([
  T('We keep FY26F NPATMI at VND10,944bn (+15.6% YoY), FY27F at VND12,674bn (+15.8%) and FY28F '
    + 'at VND14,774bn (+16.6%). Two things carry the forecast. Associate income rises to '
    + 'VND2,608bn in FY26F and VND3,449bn by FY28F, and grew 40.8% in 1H26. Operating leverage '
    + 'carries the rest: SG&A falls from 17.6% of sales to 16.5% by FY28F on an unchanged gross '
    + 'margin. ROE holds near 27% on net cash of around 60% of equity and a maintained DPS of '
    + 'VND2,000.', { size: 18 })], { after: 120 }));
children.push(P([
  T('Valuation. ', { size: 18, bold: true }),
  T('Our DCF (FCFF) target price is VND87,950. The equity risk premium stays at 9% and long-term '
    + 'growth is held at 1.5% — deliberately below what the order book alone would justify, '
    + 'to carry the risk that AI lowers IT services pricing over time. At VND71,700 the stock '
    + 'trades at 11.2x FY26F earnings against a five-year median above 18x; at the target price, '
    + '13.7x FY26F and 11.8x FY27F, implying 23% upside. We maintain BUY.', { size: 18 })],
  { after: 120 }));
children.push(P([
  T('Risks. ', { size: 18, bold: true }),
  T('(1) AI-driven price deflation outpacing our long-term growth assumption; (2) subdued US and '
    + 'global IT spending and tariff-related contract delays; (3) JPY/USD volatility, which moves '
    + 'both the translated Japanese revenue base and the FX line in financial income.',
    { size: 18 })], { after: 120 }));

children.push(P([T('Analyst certification and important disclosures follow the house template '
  + 'and are omitted from this working draft.', { size: 14, italics: true, color: GREY })],
  { after: 0 }));

const doc = new Document({
  creator: 'Mirae Asset Securities (Vietnam) Research',
  title: 'FPT Corporation - 2Q26 results review',
  styles: { default: { document: { run: { font: FONT, size: 18 } } } },
  sections: [{
    properties: { page: { size: { width: 11907, height: 16840 },
      margin: { top: 1000, bottom: 900, left: 907, right: 907 } } },
    headers: { default: new Header({ children: [P([
      T('FPT Corporation  ·  2Q26 results review  ·  Mirae Asset Vietnam Research',
        { size: 14, color: GREY })], {
      after: 0, line: 200,
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 4 } } })] }) },
    footers: { default: new Footer({ children: [new Paragraph({
      children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 13, color: GREY })],
      alignment: AlignmentType.CENTER, spacing: { before: 0, line: 200 } })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync(OUT, b);
  console.log('wrote ' + OUT + '  (' + (b.length / 1024).toFixed(0) + ' KB)');
});
