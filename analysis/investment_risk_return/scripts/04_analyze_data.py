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


results = []

for name in prices.columns:
    series = prices[name].dropna()

    daily_returns = series.pct_change().dropna()

    start_value = series.iloc[0]
    end_value = series.iloc[-1]

    start_date = series.index[0]
    end_date = series.index[-1]

    years = (end_date - start_date).days / 365.25

    total_return = (end_value / start_value) - 1

    cagr = (end_value / start_value) ** (1 / years) - 1

    annualized_volatility = daily_returns.std() * (252 ** 0.5)

    return_risk_ratio = cagr / annualized_volatility

    running_max = series.cummax()
    drawdown = (series / running_max) - 1
    max_drawdown = drawdown.min()

    drawdown_bottom_date = drawdown.idxmin()

    drawdown_peak_date = series.loc[:drawdown_bottom_date].idxmax()

    final_investment = INITIAL_INVESTMENT * (end_value / start_value)

    results.append(
        {
            "series": name,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
            "total_return_pct": total_return * 100,
            "cagr_pct": cagr * 100,
            "volatility_pct": annualized_volatility * 100,
            "return_risk_ratio": return_risk_ratio,
            "initial_investment": INITIAL_INVESTMENT,
            "final_investment": final_investment,
            "max_drawdown_pct": max_drawdown * 100,
            "drawdown_peak_date": drawdown_peak_date.date(),
            "drawdown_bottom_date": drawdown_bottom_date.date(),
        }
    )


results_df = pd.DataFrame(results)

print(results_df.to_string(index=False))

results_df.to_csv(
    PROCESSED_DIR / "summary_basic.csv",
    index=False,
)
