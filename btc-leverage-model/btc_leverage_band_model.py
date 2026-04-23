from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "Data.xlsx"
OUTPUT_PATH = BASE_DIR / "BTC_Leverage_Band_Output.xlsx"
EQUITY_FIG_PATH = BASE_DIR / "btc_leverage_band_equity.png"
LEVERAGE_FIG_PATH = BASE_DIR / "btc_leverage_band_leverage.png"

TICKER = "BTC-USD"
START_DATE = "2023-01-01"
END_DATE = "2026-01-01"

INITIAL_EQUITY = 100_000.0

PLUS_TARGET_LEVERAGE = 2.0
MINUS_TARGET_LEVERAGE = -2.0

BAND_WIDTH = 0.10


def download_btc_data() -> pd.DataFrame:
    """
    Download BTC daily price data from Yahoo Finance.
    """
    df = yf.download(
        TICKER,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,
        progress=False,
    )

    if df.empty:
        raise ValueError("No BTC data downloaded.")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    price_col = "Adj Close" if "Adj Close" in df.columns else "Close"

    data = df[[price_col]].copy()
    data = data.rename(columns={price_col: "BTC_Price"})
    data = data.dropna()
    data.index.name = "Date"
    data = data.reset_index()

    return data


def run_leverage_band_model(
    data: pd.DataFrame,
    target_leverage: float,
    band_width: float = BAND_WIDTH,
    initial_equity: float = INITIAL_EQUITY,
) -> pd.DataFrame:
    """
    Dynamic leverage band model.

    The portfolio tries to maintain target leverage.
    If leverage leaves the band, the strategy rebalances back to target leverage.
    """

    result_rows = []

    price0 = data.loc[0, "BTC_Price"]

    exposure = target_leverage * initial_equity
    shares = exposure / price0
    cash = initial_equity - exposure

    for i, row in data.iterrows():
        date = row["Date"]
        price = float(row["BTC_Price"])

        exposure_pre = shares * price
        equity_pre = cash + exposure_pre

        if equity_pre <= 0:
            result_rows.append(
                {
                    "Date": date,
                    "BTC_Price": price,
                    "Target_Leverage": target_leverage,
                    "Shares_Pre": shares,
                    "Cash_Pre": cash,
                    "Exposure_Pre": exposure_pre,
                    "Equity_Pre": equity_pre,
                    "Leverage_Pre": None,
                    "Action": "LIQUIDATED",
                    "Trade_Value": 0.0,
                    "Shares_New": shares,
                    "Cash_New": cash,
                    "Exposure_New": exposure_pre,
                    "Equity_New": equity_pre,
                    "Leverage_New": None,
                }
            )
            continue

        leverage_pre = exposure_pre / equity_pre

        lower = target_leverage - band_width
        upper = target_leverage + band_width

        if target_leverage > 0:
            outside_band = leverage_pre < lower or leverage_pre > upper
        else:
            outside_band = leverage_pre < lower or leverage_pre > upper

        if outside_band:
            target_exposure = target_leverage * equity_pre
            trade_value = target_exposure - exposure_pre

            shares_new = target_exposure / price
            cash_new = cash - trade_value
            exposure_new = shares_new * price
            equity_new = cash_new + exposure_new
            leverage_new = exposure_new / equity_new

            if trade_value > 0:
                action = "BUY / INCREASE_LONG"
            else:
                action = "SELL / INCREASE_SHORT_OR_REDUCE_LONG"
        else:
            trade_value = 0.0
            shares_new = shares
            cash_new = cash
            exposure_new = exposure_pre
            equity_new = equity_pre
            leverage_new = leverage_pre
            action = "HOLD"

        result_rows.append(
            {
                "Date": date,
                "BTC_Price": price,
                "Target_Leverage": target_leverage,
                "Shares_Pre": shares,
                "Cash_Pre": cash,
                "Exposure_Pre": exposure_pre,
                "Equity_Pre": equity_pre,
                "Leverage_Pre": leverage_pre,
                "Action": action,
                "Trade_Value": trade_value,
                "Shares_New": shares_new,
                "Cash_New": cash_new,
                "Exposure_New": exposure_new,
                "Equity_New": equity_new,
                "Leverage_New": leverage_new,
            }
        )

        shares = shares_new
        cash = cash_new

    return pd.DataFrame(result_rows)


def plot_equity(plus_df: pd.DataFrame, minus_df: pd.DataFrame) -> None:
    plt.figure(figsize=(11, 6))
    plt.plot(plus_df["Date"], plus_df["Equity_New"], label="+2x BTC leverage band model")
    plt.plot(minus_df["Date"], minus_df["Equity_New"], label="-2x BTC leverage band model")
    plt.title("BTC Dynamic Leverage Band Model: Equity Paths")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.legend()
    plt.tight_layout()
    plt.savefig(EQUITY_FIG_PATH, dpi=300)
    plt.show()


def plot_leverage(plus_df: pd.DataFrame, minus_df: pd.DataFrame) -> None:
    plt.figure(figsize=(11, 5))
    plt.plot(plus_df["Date"], plus_df["Leverage_New"], label="+2x realized leverage")
    plt.plot(minus_df["Date"], minus_df["Leverage_New"], label="-2x realized leverage")
    plt.axhline(2.0, linestyle="--", linewidth=1, label="+2x target")
    plt.axhline(-2.0, linestyle="--", linewidth=1, label="-2x target")
    plt.title("Realized Leverage After Rebalancing")
    plt.xlabel("Date")
    plt.ylabel("Leverage")
    plt.legend()
    plt.tight_layout()
    plt.savefig(LEVERAGE_FIG_PATH, dpi=300)
    plt.show()


def summarize(model_name: str, df: pd.DataFrame) -> None:
    start_equity = df["Equity_New"].iloc[0]
    final_equity = df["Equity_New"].iloc[-1]
    total_return = final_equity / start_equity - 1
    num_rebalances = (df["Action"] != "HOLD").sum()

    print(f"\n=== {model_name} Summary ===")
    print(f"Start date: {df['Date'].iloc[0].date()}")
    print(f"End date:   {df['Date'].iloc[-1].date()}")
    print(f"Initial equity: {start_equity:,.2f}")
    print(f"Final equity:   {final_equity:,.2f}")
    print(f"Total return:   {total_return:.2%}")
    print(f"Number of rebalances: {num_rebalances}")
    print(f"Min leverage: {df['Leverage_New'].min():.4f}")
    print(f"Max leverage: {df['Leverage_New'].max():.4f}")


def main() -> None:
    data = download_btc_data()
    data.to_excel(DATA_PATH, index=False)

    plus_df = run_leverage_band_model(data, target_leverage=PLUS_TARGET_LEVERAGE)
    minus_df = run_leverage_band_model(data, target_leverage=MINUS_TARGET_LEVERAGE)

    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        data.to_excel(writer, sheet_name="BTC_DATA", index=False)
        plus_df.to_excel(writer, sheet_name="PLUS_2X_BAND_MODEL", index=False)
        minus_df.to_excel(writer, sheet_name="MINUS_2X_BAND_MODEL", index=False)

    summarize("+2x BTC leverage band model", plus_df)
    summarize("-2x BTC leverage band model", minus_df)

    plot_equity(plus_df, minus_df)
    plot_leverage(plus_df, minus_df)

    print(f"\nSaved data to: {DATA_PATH}")
    print(f"Saved model output to: {OUTPUT_PATH}")
    print(f"Saved equity figure to: {EQUITY_FIG_PATH}")
    print(f"Saved leverage figure to: {LEVERAGE_FIG_PATH}")


if __name__ == "__main__":
    main()