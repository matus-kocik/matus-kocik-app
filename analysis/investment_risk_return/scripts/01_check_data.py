import yfinance as yf

tickers = {
    "USA Stocks": "^SP500TR",
    "USA Bonds": "IEF",
    "Europe Stocks": "EXSA.DE",
    "Europe Bonds": "X710.DE",
    "Germany Stocks": "^GDAXI",
    "Germany Bonds": "EXHD.DE",
}

for name, ticker in tickers.items():
    data = yf.download(
        ticker,
        start="2008-01-01",
        end="2026-01-01",
        auto_adjust=False,
        progress=False,
    )

    print(f"\n{name} ({ticker})")
    print("-" * 50)
    print("Počet záznamov:", len(data))
    print("Prvý dátum:", data.index.min())
    print("Posledný dátum:", data.index.max())
    print("Stĺpce:", list(data.columns))
