"""
Pluggable market-data providers for the daily-report charts.

A provider answers two questions for each chart:

  timeseries_point(key) -> (category, [value_per_series]) | None
      For the time-series charts (append one new point = today):
        key="pe_band"     series order: P/E, -2SD, -1SD, Average, +1SD, +2SD
        key="vnindex_fx"  series order: VN-INDEX, US$/VND (R)
        key="bond_yields" series order: 2Y, 5Y, 7Y, 10Y
        key="interbank"   series order: O/N, 1-week rate
      `category` is an Excel date serial (e.g. 1 Jan 1900 = 1). Helper below.

  category_chart(key) -> (categories, [series_values]) | None
      For the per-day charts (fully replaced each day):
        key="contributors"  categories=10 tickers; series: index impact, 1D change
        key="foreign_flows" categories=10 tickers; series: Flows (LHS), Net Flows (RHS)

Return None to leave a chart untouched.
"""
from __future__ import annotations
import csv
import datetime as _dt
from pathlib import Path


def to_excel_serial(d: _dt.date) -> int:
    """Date -> Excel serial (1900 date system, matching the deck's categories)."""
    return (d - _dt.date(1899, 12, 30)).days


# --------------------------------------------------------------------------- #
class ChartDataProvider:
    def timeseries_point(self, key):  # noqa: D401
        return None

    def category_chart(self, key):
        return None


class NoopProvider(ChartDataProvider):
    """Leaves all charts as-is (text/tables-only run)."""


# --------------------------------------------------------------------------- #
class CsvProvider(ChartDataProvider):
    """
    Reads today's chart inputs from CSV files in `data_dir`:

      timeseries.csv   key,date(YYYY-MM-DD),v1,v2,...   (one row per chart key)
      contributors.csv ticker,index_impact,one_d_change (10 rows)
      foreign_flows.csv ticker,flow,net_flow            (10 rows)

    Missing files simply skip those charts.
    """

    def __init__(self, data_dir: Path):
        self.dir = Path(data_dir)

    def timeseries_point(self, key):
        f = self.dir / "timeseries.csv"
        if not f.exists():
            return None
        for row in csv.reader(f.open()):
            if row and row[0] == key:
                date = _dt.date.fromisoformat(row[1])
                vals = [float(x) if x not in ("", "NA") else None for x in row[2:]]
                return to_excel_serial(date), vals
        return None

    def _two_series(self, fname):
        f = self.dir / fname
        if not f.exists():
            return None
        cats, a, b = [], [], []
        for row in csv.reader(f.open()):
            if not row or row[0].lower() in ("ticker", "name"):
                continue
            cats.append(row[0])
            a.append(float(row[1]))
            b.append(float(row[2]))
        return (cats, [a, b]) if cats else None

    def category_chart(self, key):
        if key == "contributors":
            return self._two_series("contributors.csv")
        if key == "foreign_flows":
            return self._two_series("foreign_flows.csv")
        return None


# --------------------------------------------------------------------------- #
class FiinQuantProvider(ChartDataProvider):
    """
    STUB. Wire this to the FiinQuant data feed once the connector is authorized.

    FiinQuant exposes Vietnamese market data (index OHLC, foreign flows by
    ticker, valuations/P-E, bond yields, interbank rates, FX) -- which is
    exactly the chart inputs. Fill in the calls below with the FiinQuant
    Python client (or the MCP tools) and return the same shapes as CsvProvider.
    """

    def __init__(self, data_dir: Path, word_fields: dict):
        self.fields = word_fields  # close/value already parsed from the Word doc
        # e.g. self.client = FiinSession(username=..., password=...).FiinIndicator()

    def timeseries_point(self, key):
        raise NotImplementedError(
            "FiinQuant provider not wired yet. Authorize the FiinQuant connector, "
            "then implement timeseries_point()/category_chart() here."
        )

    def category_chart(self, key):
        raise NotImplementedError("FiinQuant provider not wired yet.")


# --------------------------------------------------------------------------- #
def get_provider(source: str, data_dir: Path, word_fields: dict) -> ChartDataProvider:
    if source == "csv":
        return CsvProvider(data_dir)
    if source == "fiinquant":
        return FiinQuantProvider(data_dir, word_fields)
    return NoopProvider()
