from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


SERIES = {
    "usa_stocks": ("usa_stocks.csv", "Close"),
    "usa_bonds": ("usa_bonds.csv", "Adj Close"),
    "europe_stocks": ("europe_stocks.csv", "Adj Close"),
    "europe_bonds": ("europe_bonds.csv", "Adj Close"),
    "germany_stocks": ("germany_stocks.csv", "Close"),
    "germany_bonds": ("germany_bonds.csv", "Adj Close"),
}


def load_series(filename, price_column):
    path = RAW_DIR / filename

    data = pd.read_csv(
        path,
        header=[0, 1],
        index_col=0,
        parse_dates=True,
    )

    series = data[price_column].iloc[:, 0]

    return series


series_list = []

for name, (filename, price_column) in SERIES.items():
    series = load_series(filename, price_column)
    series.name = name
    series_list.append(series)

prices = pd.concat(
    series_list,
    axis=1,
    join="outer",
    sort=False,
)
prices = prices.sort_index()


prices.index.name = "date"

print(prices.info())

print("\nPrvých 5 riadkov:")
print(prices.head())

print("\nPosledných 5 riadkov:")
print(prices.tail())

print("\nChýbajúce hodnoty:")
print(prices.isna().sum())


output_path = PROCESSED_DIR / "prices.csv"
prices.to_csv(output_path)

print(f"\nUložené: {output_path}")
