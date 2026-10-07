from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


prices = pd.read_csv(
    PROCESSED_DIR / "prices.csv",
    index_col="date",
    parse_dates=True,
)


annual_returns = {}


for name in prices.columns:
    series = prices[name].dropna()

    year_end_prices = series.resample("YE").last()

    returns = year_end_prices.pct_change()

    # Rok 2008 nemá v našich dátach koniec roka 2007,
    # preto ho vypočítame od prvého dostupného dňa roku 2008.
    first_year_return = (year_end_prices.iloc[0] / series.iloc[0]) - 1
    returns.iloc[0] = first_year_return

    annual_returns[name] = returns * 100


annual_returns_df = pd.DataFrame(annual_returns)

annual_returns_df.index = annual_returns_df.index.year
annual_returns_df.index.name = "year"


output_path = PROCESSED_DIR / "annual_returns.csv"
annual_returns_df.to_csv(output_path)


print(annual_returns_df.round(2).to_string())

print(f"\nUložené: {output_path}")
