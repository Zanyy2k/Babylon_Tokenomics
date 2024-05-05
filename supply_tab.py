import pandas as pd
from helper_functions import initial_df


def calculate_monthly_issuance(row, daily_issuance):
    return pd.Timestamp(row["Date"]).daysinmonth * daily_issuance


def generate_supply_df(token_issue_date, unlock_df, daily_issuance, total_token):

    df = initial_df(token_issue_date)

    df["Monthly Issuance"] = df.apply(
        calculate_monthly_issuance, daily_issuance=daily_issuance, axis=1
    )
    df["Circulating Supply"] = (
        df["Monthly Issuance"]
        + unlock_df.set_index("Date").loc[df["Date"], "Total Unlock"].values
    )
    df["Circulating Supply"] = df["Circulating Supply"].cumsum()
    df["Total Supply"] = df["Monthly Issuance"].cumsum() + total_token
    df["Original Circulating Supply%"] = [
        f"{value * 100 :.2f}%"
        for value in df["Circulating Supply"] / df["Total Supply"]
    ]

    df["Circulating Supply after BTC Temp"] = (
        0.1 * df["Monthly Issuance"]
        + unlock_df.set_index("Date").loc[df["Date"], "Total Unlock"].values
    )
    df["Circulating Supply after BTC Temp2"] = df[
        "Circulating Supply after BTC Temp"
    ].cumsum()
    df["Monthly Issuance Shifted"] = df["Monthly Issuance"].shift(12) * 0.9

    # Initialize the 'Circulating Supply after BTC' column
    df["Circulating Supply after BTC"] = df["Circulating Supply after BTC Temp"]

    # Loop to get the value
    for i in range(12, len(df)):
        df.at[i, "Circulating Supply after BTC"] += (
            df.at[i - 1, "Circulating Supply after BTC Temp2"]
            + df.at[i, "Monthly Issuance Shifted"]
        )
        df.at[i, "Circulating Supply after BTC Temp2"] = df.at[
            i, "Circulating Supply after BTC"
        ]

    # Get the first 12 values
    df.loc[:11, "Circulating Supply after BTC"] = df[
        "Circulating Supply after BTC Temp2"
    ][:12].values

    # Drop the temporary columns
    df.drop(
        columns=[
            "Circulating Supply after BTC Temp",
            "Circulating Supply after BTC Temp2",
            "Monthly Issuance Shifted",
        ],
        inplace=True,
    )

    return df
