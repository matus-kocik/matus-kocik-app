from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


prices = pd.read_csv(
    PROCESSED_DIR / "prices.csv",
    index_col="date",
    parse_dates=True,
)


drawdown = pd.DataFrame(index=prices.index)


for name in prices.columns:
    series = prices[name].dropna()

    running_max = series.cummax()

    series_drawdown = (series / running_max - 1) * 100

    drawdown[name] = series_drawdown


drawdown.index.name = "date"


output_path = PROCESSED_DIR / "drawdown.csv"
drawdown.to_csv(output_path)


print(drawdown.round(2).tail().to_string())

print(f"\nUložené: {output_path}")
