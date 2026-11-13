# Vietnam bank KPI workbook builder

Builds an Excel KPI template for the 27 listed Vietnamese banks from FiinPro (FiinQuantX) data: asset quality, growth, efficiency and valuation, FY2014 to the latest quarter, with a bilingual (EN/VI) Search sheet, charts and QA flags.

- `bank_kpi_builder.py` — `python bank_kpi_builder.py RAW_DIR OUT.xlsx`; RAW_DIR holds raw FiinQuant MCP JSON dumps (see the docstring for file names).
- `fiinpro_export.py` — `python fiinpro_export.py TICKER RAW_DIR OUT.xlsx`; full statement/ratio/price data pack for one ticker.
- `build-prompt-chain.md` — staged prompts for building and refreshing the workbook end to end.

No FiinPro data is included: you need your own FiinPro / FiinQuantX access to pull it. Requires `openpyxl`.
