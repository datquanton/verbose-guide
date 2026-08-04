// Build the Word version of the STB + FPT note from deck_content.json, so the
// document and the slides cannot drift apart.  Run: node build_note.js
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, BorderStyle, ShadingType, HeadingLevel, PageBreak, Header, Footer,
  PageNumber, VerticalAlign,
} = require('docx');

const SRC = '/home/user/verbose-guide/deck_content.json';
const OUT = '/home/user/verbose-guide/MASVN_RS_2H26_Outlook_STB_FPT_Note_Aug2026.docx';
const data = JSON.parse(fs.readFileSync(SRC, 'utf8'));

// A4 portrait, 1.6cm side margins -> 11907 - 2*907 = 10093 dxa of text width
const TEXT_W = 10093;
const NAVY = '1F3864', GREY = '595959', RULE = 'BFBFBF', BAND = 'F2F2F2';
const FONT = 'Calibri';   // covers Vietnamese diacritics in Word and LibreOffice

const T = (text, o = {}) => new TextRun({ text, font: FONT, ...o });

const P = (text, o = {}) => new Paragraph({
  children: Array.isArray(text) ? text : [T(text, o.run || {})],
  spacing: { after: o.after === undefined ? 120 : o.after, line: o.line || 260 },
  alignment: o.align,
  ...(o.border ? { border: o.border } : {}),
  ...(o.pageBreakBefore ? { pageBreakBefore: true } : {}),
});

const cell = (children, o = {}) => new TableCell({
  children,
  width: { size: o.w, type: WidthType.DXA },
  margins: { top: 40, bottom: 40, left: 90, right: 90 },
  verticalAlign: VerticalAlign.CENTER,
  ...(o.fill ? { shading: { type: ShadingType.CLEAR, fill: o.fill, color: 'auto' } } : {}),
  ...(o.borders ? { borders: o.borders } : {}),
});

const thin = (color) => ({
  top: { style: BorderStyle.SINGLE, size: 2, color },
  bottom: { style: BorderStyle.SINGLE, size: 2, color },
  left: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
  right: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' },
});

// ---------------------------------------------------------------- FY table
function fyTable(rows) {
  const note = rows[rows.length - 1][0];          // last row is the source line
  const body = rows.slice(0, -1);
  const n = body[0].length;
  const first = 3200, rest = Math.floor((TEXT_W - first) / (n - 1));
  const widths = [first, ...Array(n - 1).fill(rest)];
  widths[n - 1] += TEXT_W - widths.reduce((a, b) => a + b, 0);

  const trs = body.map((r, ri) => new TableRow({
    children: r.map((v, ci) => cell(
      [new Paragraph({
        children: [T(v, {
          size: 16, bold: ri === 0,
          color: ri === 0 ? 'FFFFFF' : (ci >= n - 3 ? NAVY : '000000'),
        })],
        alignment: ci === 0 ? AlignmentType.LEFT : AlignmentType.RIGHT,
        spacing: { before: 20, after: 20, line: 220 },
      })],
      {
        w: widths[ci],
        fill: ri === 0 ? NAVY : (ri % 2 === 0 ? BAND : undefined),
        borders: thin(ri === 0 ? NAVY : RULE),
      },
    )),
    tableHeader: ri === 0,
  }));

  return [
    new Table({ rows: trs, columnWidths: widths, width: { size: TEXT_W, type: WidthType.DXA } }),
    P([T(note, { size: 14, italics: true, color: GREY })], { after: 200, line: 200 }),
  ];
}

// ------------------------------------------------- rating + key data block
function summaryBlock(s) {
  const half = Math.floor(TEXT_W / 2), lw = Math.floor(half * 0.56), rw = half - lw;
  const left = [...s.rating.map((r) => [r[0].replace(/\s*\n\s*/g, ' '), r[1]]),
    ['', ''],
    ...s.perf.map((r) => [r[0], r.slice(1).join('   /   ')])];
  const right = s.keydata.map((r) => [r[0], r[1]]);
  const rows = Math.max(left.length, right.length);

  const kv = (pair, w1, w2, opts = {}) => [
    cell([new Paragraph({
      children: [T(pair ? pair[0] : '', { size: 15, color: GREY, bold: opts.bold })],
      spacing: { before: 20, after: 20, line: 200 },
    })], { w: w1, borders: thin(RULE), fill: opts.fill }),
    cell([new Paragraph({
      children: [T(pair ? pair[1] : '', {
        size: 15, bold: opts.bold, color: opts.bold ? NAVY : '000000',
      })],
      alignment: AlignmentType.RIGHT,
      spacing: { before: 20, after: 20, line: 200 },
    })], { w: w2, borders: thin(RULE), fill: opts.fill }),
  ];

  const trs = [];
  for (let i = 0; i < rows; i++) {
    const hi = i < s.rating.length;   // rating rows carry the call and the TP
    trs.push(new TableRow({
      children: [
        ...kv(left[i], lw, rw, { bold: hi, fill: hi ? BAND : undefined }),
        ...kv(right[i], lw, rw),
      ],
    }));
  }
  return new Table({
    rows: trs,
    columnWidths: [lw, rw, lw, rw],
    width: { size: TEXT_W, type: WidthType.DXA },
  });
}

// ------------------------------------------------------------- one section
function section(s, first) {
  const out = [];
  out.push(new Paragraph({
    children: [T(`${s.ticker}  ·  ${s.sector}  ·  ${s.lang === 'EN' ? 'English' : 'Tiếng Việt'}`,
      { size: 15, bold: true, color: GREY, allCaps: true })],
    spacing: { after: 60, line: 200 },
    ...(first ? {} : { pageBreakBefore: true }),
  }));
  out.push(new Paragraph({
    children: [T(s.company, { size: 28, bold: true, color: NAVY })],
    spacing: { after: 40, line: 280 },
  }));
  out.push(new Paragraph({
    children: [T(s.headline, { size: 21, color: '000000' })],
    spacing: { after: 160, line: 260 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 6 } },
  }));
  out.push(summaryBlock(s));
  out.push(P('', { after: 200 }));

  out.push(new Paragraph({
    children: [T(s.points_title, { size: 20, bold: true, color: NAVY })],
    spacing: { after: 100, line: 240 },
  }));
  // A short paragraph is a run-in heading for the one that follows it.
  s.points.forEach((t) => {
    const head = t.length < 120 && t.trim().endsWith(':');
    out.push(new Paragraph({
      children: [T(t.trim(), { size: 17, bold: head, color: head ? NAVY : '000000' })],
      alignment: head ? AlignmentType.LEFT : AlignmentType.JUSTIFIED,
      spacing: { after: head ? 40 : 140, line: 250 },
    }));
  });

  out.push(P('', { after: 60 }));
  out.push(...fyTable(s.fy));
  out.push(P([T(s.analyst, { size: 15, color: GREY })], { after: 0, line: 200 }));
  return out;
}

// ------------------------------------------------------------------ cover
const cover = [
  P([T('Mirae Asset Securities (Vietnam)  ·  Research', { size: 16, bold: true, color: GREY, allCaps: true })],
    { after: 80 }),
  new Paragraph({
    children: [T('2H26 Equity Outlook — Vietnam', { size: 40, bold: true, color: NAVY })],
    spacing: { after: 60, line: 400 },
  }),
  new Paragraph({
    children: [T('STB · FPT  —  2Q26 results review and forecast revision', { size: 24, color: '000000' })],
    spacing: { after: 200, line: 300 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 8 } },
  }),
  P([T('4 August 2026', { size: 18, color: GREY })], { after: 300 }),
];

const summaryRows = [
  ['Ticker', 'Rating', 'Target price (VND)', 'Current price (VND)', 'Expected return'],
  ...data.filter((s) => s.lang === 'EN').map((s) => [
    s.ticker, s.rating[0][1], s.rating[1][1], s.rating[2][1], s.rating[3][1],
  ]),
];
{
  const n = 5, first = 1600, rest = Math.floor((TEXT_W - first) / (n - 1));
  const widths = [first, ...Array(n - 1).fill(rest)];
  widths[n - 1] += TEXT_W - widths.reduce((a, b) => a + b, 0);
  cover.push(new Table({
    rows: summaryRows.map((r, ri) => new TableRow({
      children: r.map((v, ci) => cell([new Paragraph({
        children: [T(v, { size: 17, bold: ri === 0 || ci === 0 || ci === 1, color: ri === 0 ? 'FFFFFF' : (ci === 1 ? NAVY : '000000') })],
        alignment: ci === 0 ? AlignmentType.LEFT : AlignmentType.RIGHT,
        spacing: { before: 40, after: 40, line: 230 },
      })], { w: widths[ci], fill: ri === 0 ? NAVY : undefined, borders: thin(ri === 0 ? NAVY : RULE) })),
      tableHeader: ri === 0,
    })),
    columnWidths: widths,
    width: { size: TEXT_W, type: WidthType.DXA },
  }));
  cover.push(P([T('Prices as at the dates shown in each section. Source: Mirae Asset Vietnam Research',
    { size: 14, italics: true, color: GREY })], { after: 240, line: 200 }));
  cover.push(P([T('Contents', { size: 20, bold: true, color: NAVY })], { after: 80 }));
  data.forEach((s, i) => cover.push(P([
    T(`${i + 1}.  ${s.ticker} — ${s.lang === 'EN' ? 'English' : 'Tiếng Việt'}   `, { size: 17, bold: true }),
    T(s.headline, { size: 17, color: GREY }),
  ], { after: 40, line: 230 })));
}

const children = [...cover];
data.forEach((s) => children.push(...section(s, false)));

const doc = new Document({
  creator: 'Mirae Asset Securities (Vietnam) Research',
  title: '2H26 Equity Outlook — Vietnam: STB and FPT',
  description: '2Q26 results review and forecast revision',
  styles: { default: { document: { run: { font: FONT, size: 17 } } } },
  sections: [{
    properties: {
      page: {
        size: { width: 11907, height: 16840 },              // A4 portrait
        margin: { top: 1000, bottom: 1000, left: 907, right: 907 },
      },
    },
    headers: {
      default: new Header({
        children: [P([
          T('Mirae Asset Securities (Vietnam)  ·  2H26 Equity Outlook  ·  STB · FPT',
            { size: 14, color: GREY }),
        ], {
          after: 0, line: 200,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 4 } },
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          children: [
            T('Analyst certification and important disclosures are at the end of this report.   ',
              { size: 13, color: GREY }),
            new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 13, color: GREY }),
          ],
          alignment: AlignmentType.CENTER,
          spacing: { before: 0, line: 200 },
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync(OUT, b);
  console.log('wrote ' + OUT + '  (' + (b.length / 1024).toFixed(0) + ' KB)');
});
