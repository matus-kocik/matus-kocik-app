from pathlib import Path

import yfinance as yf

START_DATE = "2008-01-01"
END_DATE = "2026-01-01"

TICKERS = {
    "usa_stocks": "^SP500TR",
    "usa_bonds": "IEF",
    "europe_stocks": "EXSA.DE",
    "europe_bonds": "X710.DE",
    "germany_stocks": "^GDAXI",
    "germany_bonds": "EXHD.DE",
}

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


for name, ticker in TICKERS.items():
    print(f"Sťahujem {name} ({ticker})...")

    data = yf.download(
        ticker,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,
        progress=False,
    )

    output_path = RAW_DIR / f"{name}.csv"
    data.to_csv(output_path)

    print(f"Uložené: {output_path}")
