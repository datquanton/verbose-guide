# Nghiên cứu cổ phiếu Việt Nam: website

This branch is the website at vneconomy.site (Vercel project `equity-research-thesis-to-portfolio`, production branch `site`).
Do not edit it here: it is generated in the owner's research vault (`Workshop/Deliverables/research-site-build/`, `publish.sh`) and copied in.

| Path | What |
|---|---|
| `/` and `/en/` | Homepages (Vietnamese, English), one heading per section |
| `/vi-mo/` | Macro |
| `/nganh/` | Sector reports, banks included |
| `/ket-qua-kinh-doanh/` | Earnings reviews |
| `/assets/` | House stylesheet and script shared by every page |
| `/huong-dan/` | Guides |
| `/danh-muc/` | Portfolio consultant (interactive tool; `en/` for English). **Hand-built on this branch, not generated**: register it with the site generator before the next `publish.sh`, or the copy-in may drop it and the homepage links to it. See `danh-muc/README.md` |
| other folders | Redirects only, for links shared before pages moved |

Every report sits at `/<section>/<topic>-<period>/` (for example `/nganh/chung-khoan-3q26/`); a second language is a subfolder (`en/`).

Personal research, not investment advice. Updated 2026-11-13.
