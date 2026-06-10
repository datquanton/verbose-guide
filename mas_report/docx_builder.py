"""Assemble the .docx.

Two modes:
  * build_fresh()    -- standalone doc with heading, narrative, and a data table.
  * fill_template()  -- replace a {{NARRATIVE}} placeholder inside an existing
                        MAS template .docx (keeps your branding/tables intact).
"""

from __future__ import annotations

from .compute import ReportMetrics


def _data_rows(m: ReportMetrics):
    return [
        ("Open", m.open_pts, m.open_dod),
        ("High", m.high_pts, m.high_dod),
        ("Low", m.low_pts, m.low_dod),
        ("Close", m.close_pts, m.close_dod),
        ("Matched volume", m.volume_str, m.volume_dod),
        ("Matched value", m.value_str, m.value_dod),
    ]


def build_fresh(m: ReportMetrics, narrative: str, out_path: str, title: str = "Vietnam Stock Market"):
    from docx import Document

    doc = Document()
    doc.add_heading(title, level=1)
    doc.add_paragraph(f"Session: {m.date}").italic = True

    table = doc.add_table(rows=1, cols=3)
    table.style = "Light Grid Accent 1"
    hdr = table.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Metric", "Value", "DoD"
    for label, value, dod in _data_rows(m):
        cells = table.add_row().cells
        cells[0].text, cells[1].text, cells[2].text = label, value, dod

    doc.add_paragraph()
    for block in narrative.split("\n\n"):
        doc.add_paragraph(block)

    doc.save(out_path)
    return out_path


def fill_template(template_path: str, narrative: str, out_path: str,
                  placeholder: str = "{{NARRATIVE}}"):
    """Replace `placeholder` (in body paragraphs or table cells) with the
    narrative paragraphs, preserving the rest of the template."""
    from docx import Document

    doc = Document(template_path)
    blocks = narrative.split("\n\n")

    def _replace_in_paragraph(par):
        if placeholder not in par.text:
            return False
        # clear existing runs, write first block, append rest as new paragraphs
        for run in list(par.runs):
            run.text = ""
        if par.runs:
            par.runs[0].text = blocks[0]
        else:
            par.add_run(blocks[0])
        for extra in blocks[1:]:
            new = par.insert_paragraph_before(extra)  # keep order via before-insertions
        return True

    replaced = any(_replace_in_paragraph(p) for p in doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if _replace_in_paragraph(p):
                        replaced = True
    if not replaced:
        raise ValueError(f"placeholder {placeholder!r} not found in {template_path}")
    doc.save(out_path)
    return out_path
