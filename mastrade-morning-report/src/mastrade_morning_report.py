from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import urllib3
from docx import Document
from docx.shared import Inches, Pt


BASE_URL = "https://mastrade.masvn.com"
DEFAULT_INDEX = "VN-INDEX"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
)



@dataclass
class StockValue:
    symbol: str
    value_billion: float


@dataclass
class ReportData:
    generated_at: str
    index_symbol: str
    index_value: float
    index_change: float
    index_change_pct: float
    pe: str
    pb: str
    market_cap_billion: float | None
    total_foreign_buy_billion: float | None
    total_foreign_sell_billion: float | None
    volume_shares: int
    value_vnd: int
    volume_change_pct: float | None
    value_change_pct: float | None
    top_gainers: list[str]
    top_losers: list[str]
    foreign_net_billion: float
    foreign_net_buy: list[StockValue]
    foreign_net_sell: list[StockValue]


class MastradeClient:
    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "application/json, text/plain, */*",
                "Referer": f"{self.base_url}/market/market-watch",
            }
        )

    def get_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        try:
            response = self.session.get(url, params=params, timeout=30)
        except requests.exceptions.SSLError:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = self.session.get(url, params=params, timeout=30, verify=False)
        response.raise_for_status()
        return response.json()

    def graphql_query(self, path: str, name: str, query: dict[str, Any], fields: list[str]) -> Any:
        query_text = build_mastrade_query(name, query, fields)
        return self.get_json(path, {"query": query_text})

    def quote(self, symbol: str) -> dict[str, Any]:
        payload = self.get_json(f"/api/v1/market/{symbol}/quote")
        rows = payload.get("data") or []
        if not rows:
            raise RuntimeError(f"Khong tim thay du lieu quote cho {symbol}")
        return rows[0]

    def stock_influence(self, index: str, sort_type: str, count: int) -> list[dict[str, Any]]:
        return self.graphql_query(
            "/api/v2/vs/stockInfluence",
            "vsStockInfluenceList",
            {
                "IndexCode": index,
                "fetchCount": count,
                "SortType": sort_type,
                "SortBy": "InfluenceIndex",
            },
            ["StockCode", "InfluenceIndex", "InfluencePercent", "Change", "PerChange"],
        )

    def foreign_total(self) -> float:
        payload = self.graphql_query(
            "/api/v2/vs/foreignHistory",
            "vsForeignTotal",
            {"range": "1D"},
            ["NetBuyVal"],
        )
        return float(payload.get("NetBuyVal") or 0)

    def foreign_top(self, top_code: str, count: int) -> list[dict[str, Any]]:
        return self.get_json("/api/v1/market/top", {"top": top_code, "fetchCount": count})

    def detail_index(self, symbol: str) -> dict[str, Any]:
        rows = self.graphql_query(
            "/api/v2/vs/detailIndex",
            "vsDetailIndex",
            {"fetchCount": 1, "symbol": symbol},
            [
                "symbol",
                "TradingDate",
                "PE",
                "PB",
                "Max52WCloseIndex",
                "Min52WCloseIndex",
                "TotalForeignBuyVal",
                "TotalForeignSellVal",
                "MarketCapital",
            ],
        )
        return rows[0] if rows else {}


def build_mastrade_query(name: str, query: dict[str, Any], fields: list[str]) -> str:
    args = ",".join(f"{key}:{json.dumps(value, ensure_ascii=False)}" for key, value in query.items())
    field_text = ",".join(fields)
    return f"query{{{name}({args}){{{field_text}}}}}"


def vnd_to_billion(value: float | int | None) -> float:
    return float(value or 0) / 1_000_000_000


def pct_change(current: float, previous: float | None) -> float | None:
    if previous in (None, 0):
        return None
    return (current - previous) / previous * 100


def load_previous_snapshot(snapshot_dir: Path, current_date: str) -> dict[str, Any] | None:
    if not snapshot_dir.exists():
        return None
    candidates = sorted(
        path for path in snapshot_dir.glob("*.json") if not path.name.startswith(current_date)
    )
    if not candidates:
        return None
    return json.loads(candidates[-1].read_text(encoding="utf-8"))


def save_snapshot(snapshot_dir: Path, data: ReportData) -> Path:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("%Y-%m-%d_%H%M%S.json")
    path = snapshot_dir / filename
    payload = asdict(data)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def collect_report_data(args: argparse.Namespace) -> ReportData:
    client = MastradeClient(args.base_url)
    quote = client.quote(args.index)
    try:
        detail_index = client.detail_index(args.index)
    except requests.RequestException:
        detail_index = {}

    now = datetime.now()
    previous = load_previous_snapshot(Path(args.snapshot_dir), now.strftime("%Y-%m-%d"))
    previous_volume = previous.get("volume_shares") if previous else None
    previous_value = previous.get("value_vnd") if previous else None

    foreign_buy = to_foreign_values(
        client.foreign_top("TOP_FOREIGN_NET_BUY_VALUE", args.foreign_count),
        positive=True,
    )
    foreign_sell = to_foreign_values(
        client.foreign_top("TOP_FOREIGN_NET_SELL_VALUE", args.foreign_count),
        positive=False,
    )

    volume = int(quote.get("vo") or 0)
    value = int(quote.get("va") or 0)

    return ReportData(
        generated_at=now.isoformat(timespec="seconds"),
        index_symbol=args.index,
        index_value=float(quote.get("c") or 0),
        index_change=float(quote.get("ch") or 0),
        index_change_pct=float(quote.get("r") or 0) * 100,
        pe=format_optional_number(detail_index.get("PE"), args.pe),
        pb=format_optional_number(detail_index.get("PB"), "N/A"),
        market_cap_billion=vnd_to_billion(detail_index.get("MarketCapital"))
        if detail_index.get("MarketCapital") is not None
        else None,
        total_foreign_buy_billion=vnd_to_billion(detail_index.get("TotalForeignBuyVal"))
        if detail_index.get("TotalForeignBuyVal") is not None
        else None,
        total_foreign_sell_billion=vnd_to_billion(detail_index.get("TotalForeignSellVal"))
        if detail_index.get("TotalForeignSellVal") is not None
        else None,
        volume_shares=volume,
        value_vnd=value,
        volume_change_pct=pct_change(volume, previous_volume),
        value_change_pct=pct_change(value, previous_value),
        top_gainers=[row["StockCode"] for row in client.stock_influence(args.index, "DESC", args.influence_count)],
        top_losers=[row["StockCode"] for row in client.stock_influence(args.index, "ASC", args.influence_count)],
        foreign_net_billion=vnd_to_billion(client.foreign_total()),
        foreign_net_buy=foreign_buy,
        foreign_net_sell=foreign_sell,
    )


def to_foreign_values(rows: list[dict[str, Any]], positive: bool) -> list[StockValue]:
    result: list[StockValue] = []
    for row in rows:
        buy = float(row.get("frBva") or 0)
        sell = float(row.get("frSva") or 0)
        value = buy - sell
        if positive:
            value = max(value, 0)
        else:
            value = abs(min(value, 0))
        result.append(StockValue(symbol=row.get("s", ""), value_billion=vnd_to_billion(value)))
    return result


def fmt_number(value: float, digits: int = 1) -> str:
    if math.isclose(value, round(value), abs_tol=10**-digits):
        return f"{round(value):,.0f}"
    return f"{value:,.{digits}f}"


def fmt_pct(value: float | None, signed: bool = True, digits: int = 1) -> str:
    if value is None:
        return "N/A"
    sign = "+" if signed and value > 0 else ""
    return f"{sign}{fmt_number(value, digits)}%"


def fmt_billion(value: float) -> str:
    return fmt_number(value, 0)


def format_optional_number(value: Any, fallback: str = "N/A", digits: int = 2) -> str:
    if value in (None, ""):
        return fallback
    try:
        return fmt_number(float(value), digits)
    except (TypeError, ValueError):
        return str(value)


def stock_list_text(items: list[StockValue]) -> str:
    return ", ".join(f"{item.symbol} ({fmt_billion(item.value_billion)} tỷ)" for item in items)


def configure_document(document: Document) -> None:
    section = document.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.45)
    section.right_margin = Inches(1)

    style = document.styles["Normal"]
    style.font.name = "Noto Sans"
    style.font.size = Pt(12)
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.15


def add_text(document: Document, text: str) -> None:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(0)
    run = paragraph.add_run(text)
    run.font.name = "Noto Sans"
    run.font.size = Pt(12)


def add_runs(document: Document, parts: list[tuple[str, bool]]) -> None:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(0)
    for text, bold in parts:
        run = paragraph.add_run(text)
        run.bold = bold
        run.font.name = "Noto Sans"
        run.font.size = Pt(12)


def add_blank(document: Document) -> None:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_after = Pt(0)


def build_docx(data: ReportData, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document = Document()
    configure_document(document)

    add_runs(document, [("NOTI:", True)])
    add_text(
        document,

        f"{data.index_symbol} {fmt_number(data.index_value, 2)} điểm ("
        f"{fmt_pct(data.index_change_pct, signed=True, digits=2)})",
    )

    add_runs(document, [("P/E: ", False), (str(data.pe), True), (" (Bloomberg)", False)])
    add_runs(
        document,
        [
            ("Khối lượng giao dịch: ", False),
            (f"{fmt_number(data.volume_shares / 1_000_000, 0)} triệu CP", True),
            (f" ({fmt_pct(data.volume_change_pct)} DoD)", False),
        ],
    )
    add_runs(
        document,
        [
            ("Giá trị GD: ", False),
            (f"{fmt_number(data.value_vnd / 1_000_000_000, 0)} tỷ", True),
            (f" ({fmt_pct(data.value_change_pct)} DoD)", False),
        ],
    )
    add_text(document, "Top các cổ phiếu ảnh hưởng đến thị trường:")
    add_text(document, f"+ Chiều tăng điểm: {', '.join(data.top_gainers)}")
    add_text(document, f"+ Chiều giảm điểm: {', '.join(data.top_losers)}")

    foreign_action = "Mua ròng" if data.foreign_net_billion >= 0 else "Bán ròng"
    add_runs(
        document,
        [
            ("Khối ngoại ", False),
            (f"{foreign_action} {fmt_billion(abs(data.foreign_net_billion))} tỷ", True),
            (", trong đó:", False),
        ],
    )
    add_text(document, f"+ Mua ròng: {stock_list_text(data.foreign_net_buy)}")
    add_text(document, f"+ Bán ròng: {stock_list_text(data.foreign_net_sell)}")

    add_blank(document)
    add_blank(document)
    add_text(document, "ROOM MG")
    add_blank(document)
    add_text(document, "Phòng Research gửi Anh/ Chị tóm tắt phiên giao dịch buổi sáng:")
    add_text(
        document,

        f"• Kết thúc phiên giao dịch buổi sáng, chỉ số {data.index_symbol} đóng cửa ở mức "
        f"{fmt_number(data.index_value, 2)} điểm, {change_word(data.index_change)} "
        f"{fmt_number(abs(data.index_change), 2)} điểm ({fmt_pct(data.index_change_pct, signed=True, digits=2)})",
    )

    add_text(document, f"• P/E {data.index_symbol} ở mức {data.pe} (Bloomberg)")
    add_text(
        document,

        f"• Khối lượng giao dịch: {fmt_number(data.volume_shares / 1_000_000, 0)} triệu CP ("
        f"{fmt_pct(data.volume_change_pct)} so với sáng trước đó).",
    )

    add_text(
        document,

        f"• Giá trị GD: {fmt_number(data.value_vnd / 1_000_000_000, 0)} tỷ ("

        f"{fmt_pct(data.value_change_pct)} so với sáng trước đó)",
    )

    add_text(document, "• Top các cổ phiếu ảnh hưởng đến thị trường:")
    add_text(document, f"+ Chiều tăng điểm: {', '.join(data.top_gainers)}")
    add_text(document, f"+ Chiều giảm điểm: {', '.join(data.top_losers)}")
    add_text(
        document,
        f"• Khối ngoại {foreign_action.lower()} {fmt_billion(abs(data.foreign_net_billion))} tỷ, trong đó:",
    )
    add_text(document, f"+ Mua ròng: {stock_list_text(data.foreign_net_buy)}")
    add_text(document, f"+ Bán ròng: {stock_list_text(data.foreign_net_sell)}")

    document.save(output_path)


def change_word(value: float) -> str:
    if value > 0:
        return "tăng"
    if value < 0:
        return "giảm"
    return "không đổi"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tao bao cao Word tom tat phien sang tu MAStrade.")
    parser.add_argument("--base-url", default=BASE_URL)
    parser.add_argument("--index", default=DEFAULT_INDEX)
    parser.add_argument("--pe", default="N/A", help="P/E VN-Index theo Bloomberg; MAStrade khong cung cap truong nay.")
    parser.add_argument("--influence-count", type=int, default=5)
    parser.add_argument("--foreign-count", type=int, default=4)
    parser.add_argument("--snapshot-dir", default="data/snapshots")
    parser.add_argument("--output", default=None)
    parser.add_argument("--no-save-snapshot", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = collect_report_data(args)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = Path(args.output) if args.output else Path("output") / f"morning_report_{timestamp}.docx"
    build_docx(data, output)
    if not args.no_save_snapshot:
        save_snapshot(Path(args.snapshot_dir), data)
    print(f"Created: {output.resolve()}")


if __name__ == "__main__":
    main()
