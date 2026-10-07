from pathlib import Path

import pandas as pd
from django.views.generic import TemplateView


class InvestmentRiskReturnView(TemplateView):
    template_name = "investicie/investicie.html"

    ASSET_NAMES = {
        "usa_stocks": "USA – akcie",
        "usa_bonds": "USA – dlhopisy",
        "europe_stocks": "Európa – akcie",
        "europe_bonds": "Európa – dlhopisy",
        "germany_stocks": "Nemecko – akcie",
        "germany_bonds": "Nemecko – dlhopisy",
    }

    SERIES_COLUMNS = [
        "usa_stocks",
        "usa_bonds",
        "europe_stocks",
        "europe_bonds",
        "germany_stocks",
        "germany_bonds",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base_dir = Path(__file__).resolve().parent.parent
        processed_dir = (
            base_dir / "analysis" / "investment_risk_return" / "data" / "processed"
        )

        # =====================================================
        # BASIC RESULTS
        # =====================================================

        results = pd.read_csv(processed_dir / "summary_basic.csv")

        results["display_name"] = results["series"].map(self.ASSET_NAMES)
        results["display_name"] = results["display_name"].fillna(results["series"])

        context["results"] = results.to_dict(orient="records")

        # =====================================================
        # SUMMARY DATA FOR CHARTS
        # =====================================================

        summary_columns = [
            "series",
            "cagr_pct",
            "volatility_pct",
            "return_risk_ratio",
            "final_investment",
            "max_drawdown_pct",
        ]

        summary_data = results[summary_columns].copy()

        summary_data = summary_data.astype(object)
        summary_data = summary_data.where(
            pd.notna(summary_data),
            None,
        )

        context["summary_data"] = summary_data.to_dict(orient="records")

        # =====================================================
        # INVESTMENT GROWTH
        # =====================================================

        investment_growth = pd.read_csv(
            processed_dir / "investment_growth.csv",
            parse_dates=["date"],
        )

        context["growth_dates"] = [
            date.strftime("%Y-%m-%d") for date in investment_growth["date"]
        ]

        growth_data = investment_growth[self.SERIES_COLUMNS].copy()

        growth_data = growth_data.astype(object)
        growth_data = growth_data.where(
            pd.notna(growth_data),
            None,
        )

        context["growth_series"] = {
            column: growth_data[column].tolist() for column in self.SERIES_COLUMNS
        }

        # =====================================================
        # ANNUAL RETURNS
        # =====================================================

        annual_returns = pd.read_csv(processed_dir / "annual_returns.csv")

        context["annual_years"] = annual_returns["year"].astype(int).tolist()

        annual_data = annual_returns[self.SERIES_COLUMNS].copy()

        annual_data = annual_data.astype(object)
        annual_data = annual_data.where(
            pd.notna(annual_data),
            None,
        )

        context["annual_series"] = {
            column: annual_data[column].tolist() for column in self.SERIES_COLUMNS
        }

        # =====================================================
        # DRAWDOWN
        # =====================================================

        drawdown = pd.read_csv(
            processed_dir / "drawdown.csv",
            parse_dates=["date"],
        )

        context["drawdown_dates"] = [
            date.strftime("%Y-%m-%d") for date in drawdown["date"]
        ]

        drawdown_data = drawdown[self.SERIES_COLUMNS].copy()

        drawdown_data = drawdown_data.astype(object)
        drawdown_data = drawdown_data.where(
            pd.notna(drawdown_data),
            None,
        )

        context["drawdown_series"] = {
            column: drawdown_data[column].tolist() for column in self.SERIES_COLUMNS
        }

        # =====================================================
        # HELPER
        # =====================================================

        def group_summary(dataframe):
            return {
                "cagr_pct": dataframe["cagr_pct"].mean(),
                "volatility_pct": dataframe["volatility_pct"].mean(),
                "return_risk_ratio": dataframe["return_risk_ratio"].mean(),
                "max_drawdown_pct": dataframe["max_drawdown_pct"].mean(),
                "final_investment": dataframe["final_investment"].mean(),
            }

        # =====================================================
        # SUMMARY — ASSET CLASSES
        # =====================================================

        stocks = results[
            results["series"].isin(
                [
                    "usa_stocks",
                    "europe_stocks",
                    "germany_stocks",
                ]
            )
        ]

        bonds = results[
            results["series"].isin(
                [
                    "usa_bonds",
                    "europe_bonds",
                    "germany_bonds",
                ]
            )
        ]

        context["asset_class_summary"] = {
            "stocks": group_summary(stocks),
            "bonds": group_summary(bonds),
        }

        # =====================================================
        # SUMMARY — REGIONS
        # =====================================================

        regions = {
            "USA": results[
                results["series"].isin(
                    [
                        "usa_stocks",
                        "usa_bonds",
                    ]
                )
            ],
            "Európa": results[
                results["series"].isin(
                    [
                        "europe_stocks",
                        "europe_bonds",
                    ]
                )
            ],
            "Nemecko": results[
                results["series"].isin(
                    [
                        "germany_stocks",
                        "germany_bonds",
                    ]
                )
            ],
        }

        context["region_summary"] = [
            {
                "name": region_name,
                **group_summary(region_data),
            }
            for region_name, region_data in regions.items()
        ]

        # =====================================================
        # ANALYSIS CONCLUSION
        # =====================================================

        highest_return = results.loc[results["cagr_pct"].idxmax()].to_dict()

        lowest_volatility = results.loc[results["volatility_pct"].idxmin()].to_dict()

        best_return_risk = results.loc[results["return_risk_ratio"].idxmax()].to_dict()

        highest_final_value = results.loc[
            results["final_investment"].idxmax()
        ].to_dict()

        deepest_drawdown = results.loc[results["max_drawdown_pct"].idxmin()].to_dict()

        smallest_drawdown = results.loc[results["max_drawdown_pct"].idxmax()].to_dict()

        context["analysis_conclusion"] = {
            "highest_return": highest_return,
            "lowest_volatility": lowest_volatility,
            "best_return_risk": best_return_risk,
            "highest_final_value": highest_final_value,
            "deepest_drawdown": deepest_drawdown,
            "smallest_drawdown": smallest_drawdown,
        }

        return context
