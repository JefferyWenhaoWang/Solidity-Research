import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


def download_btc_data(start: str = "2023-01-01", end: str = "2026-01-01") -> pd.DataFrame:
    """
    Download daily BTC price data from Yahoo Finance.
    """
    df = yf.download("BTC-USD", start=start, end=end, auto_adjust=False)

    if df.empty:
        raise ValueError("No data downloaded. Check your internet connection or ticker symbol.")

    # Keep only close price
    if "Close" not in df.columns:
        raise ValueError("Downloaded data does not contain a 'Close' column.")

    df = df[["Close"]].copy()
    df.rename(columns={"Close": "btc_close"}, inplace=True)

    # Daily return
    df["btc_return"] = df["btc_close"].pct_change()
    df = df.dropna().copy()

    return df


def simulate_leveraged_paths(df: pd.DataFrame, initial_value: float = 100.0) -> pd.DataFrame:
    """
    Simulate 1x, +2x, and -2x daily reset products.
    """
    out = df.copy()

    out["ret_1x"] = out["btc_return"]
    out["ret_plus_2x"] = 2.0 * out["btc_return"]
    out["ret_minus_2x"] = -2.0 * out["btc_return"]

    # IMPORTANT:
    # If BTC daily return is below -50%, then 2x product would mathematically go <= 0.
    # We clip at -99.9% to keep the simulation numerically stable.
    out["ret_plus_2x"] = out["ret_plus_2x"].clip(lower=-0.999)
    out["ret_minus_2x"] = out["ret_minus_2x"].clip(lower=-0.999)

    out["nav_btc_1x"] = initial_value * (1 + out["ret_1x"]).cumprod()
    out["nav_plus_2x"] = initial_value * (1 + out["ret_plus_2x"]).cumprod()
    out["nav_minus_2x"] = initial_value * (1 + out["ret_minus_2x"]).cumprod()

    return out


def print_summary(df: pd.DataFrame) -> None:
    """
    Print a short summary for your write-up.
    """
    final_1x = df["nav_btc_1x"].iloc[-1]
    final_plus_2x = df["nav_plus_2x"].iloc[-1]
    final_minus_2x = df["nav_minus_2x"].iloc[-1]

    total_return_1x = final_1x / df["nav_btc_1x"].iloc[0] - 1
    total_return_plus_2x = final_plus_2x / df["nav_plus_2x"].iloc[0] - 1
    total_return_minus_2x = final_minus_2x / df["nav_minus_2x"].iloc[0] - 1

    print("\n=== Simulation Summary ===")
    print(f"Sample period: {df.index.min().date()} to {df.index.max().date()}")
    print(f"BTC 1x final NAV: {final_1x:.2f} | total return: {total_return_1x:.2%}")
    print(f"+2x final NAV:    {final_plus_2x:.2f} | total return: {total_return_plus_2x:.2%}")
    print(f"-2x final NAV:    {final_minus_2x:.2f} | total return: {total_return_minus_2x:.2%}")

    daily_vol = df["btc_return"].std()
    print(f"BTC daily return std dev: {daily_vol:.4%}")


def plot_navs(df: pd.DataFrame) -> None:
    """
    Plot cumulative NAV paths.
    """
    plt.figure(figsize=(11, 6))
    plt.plot(df.index, df["nav_btc_1x"], label="BTC 1x")
    plt.plot(df.index, df["nav_plus_2x"], label="Simulated +2x")
    plt.plot(df.index, df["nav_minus_2x"], label="Simulated -2x")
    plt.title("BTC vs Simulated Daily Reset +2x and -2x")
    plt.xlabel("Date")
    plt.ylabel("NAV")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_returns(df: pd.DataFrame) -> None:
    """
    Plot BTC daily returns to visualize volatility/path dependence.
    """
    plt.figure(figsize=(11, 4))
    plt.plot(df.index, df["btc_return"])
    plt.title("BTC Daily Returns")
    plt.xlabel("Date")
    plt.ylabel("Daily Return")
    plt.tight_layout()
    plt.show()


def run_path_examples(initial_value: float = 100.0) -> None:
    """
    Optional toy examples to show attrition clearly.
    """
    examples = {
        "Oscillating path": [0.05, -0.05, 0.04, -0.04, 0.03, -0.03],
        "Upward trend": [0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
        "Downward trend": [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01],
    }

    print("\n=== Toy Path Examples ===")

    for name, returns in examples.items():
        temp = pd.DataFrame({"r": returns})
        temp["ret_1x"] = temp["r"]
        temp["ret_plus_2x"] = (2 * temp["r"]).clip(lower=-0.999)
        temp["ret_minus_2x"] = (-2 * temp["r"]).clip(lower=-0.999)

        temp["nav_1x"] = initial_value * (1 + temp["ret_1x"]).cumprod()
        temp["nav_plus_2x"] = initial_value * (1 + temp["ret_plus_2x"]).cumprod()
        temp["nav_minus_2x"] = initial_value * (1 + temp["ret_minus_2x"]).cumprod()

        print(f"\n{name}")
        print(f"1x final NAV:   {temp['nav_1x'].iloc[-1]:.2f}")
        print(f"+2x final NAV:  {temp['nav_plus_2x'].iloc[-1]:.2f}")
        print(f"-2x final NAV:  {temp['nav_minus_2x'].iloc[-1]:.2f}")


def main() -> None:
    # You can change the dates here
    start_date = "2023-01-01"
    end_date = "2026-01-01"

    df = download_btc_data(start=start_date, end=end_date)
    sim_df = simulate_leveraged_paths(df, initial_value=100.0)

    print_summary(sim_df)
    run_path_examples(initial_value=100.0)

    plot_navs(sim_df)
    plot_returns(sim_df)


if __name__ == "__main__":
    main()