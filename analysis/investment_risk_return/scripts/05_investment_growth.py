from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

INITIAL_INVESTMENT = 10_000


prices = pd.read_csv(
    PROCESSED_DIR / "prices.csv",
    index_col="date",
    parse_dates=True,
)


investment_growth = pd.DataFrame(index=prices.index)


for name in prices.columns:
    series = prices[name].dropna()

    normalized = series / series.iloc[0]

    investment_growth[name] = normalized * INITIAL_INVESTMENT


investment_growth.index.name = "date"

output_path = PROCESSED_DIR / "investment_growth.csv"
investment_growth.to_csv(output_path)


print("Prvých 5 riadkov:")
print(investment_growth.head())

print("\nPosledných 5 riadkov:")
print(investment_growth.tail())

print(f"\nUložené: {output_path}")
