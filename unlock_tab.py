import pandas as pd
from helper_functions import initial_df


def calculate_stake_drops(row, token_issue_date, stake_drops_total):

    if token_issue_date <= row["Date"] < (token_issue_date + pd.DateOffset(years=1)).date():
        return int(stake_drops_total / 12 / 2)
    elif (
        (token_issue_date + pd.DateOffset(years=1)).date()
        <= row["Date"]
        < (token_issue_date + pd.DateOffset(years=2)).date()
    ):
        return stake_drops_total / 48
    elif row["Date"] >= (token_issue_date + pd.DateOffset(years=2)).date():
        return stake_drops_total / 96
    else:
        return row["Stake Drops"]


def calculate_future_community_incentives(
    row, token_issue_date, future_community_incentives_total
):
    if token_issue_date <= row["Date"] < (token_issue_date + pd.DateOffset(years=1)).date():
        return 0
    elif row["Date"] >= (token_issue_date + pd.DateOffset(years=1)).date():
        return future_community_incentives_total / 36


def calculate_investor(row, token_issue_date, investor_total):
    if token_issue_date <= row["Date"] < (token_issue_date + pd.DateOffset(years=1)).date():
        return 0
    elif row["Date"] >= (token_issue_date + pd.DateOffset(years=1)).date():
        return investor_total / 36


def calculate_early_contributors(row, token_issue_date, early_contributors_total):
    if token_issue_date <= row["Date"] < (token_issue_date + pd.DateOffset(years=1)).date():
        return 0
    elif row["Date"] >= (token_issue_date + pd.DateOffset(years=1)).date():
        return early_contributors_total / 36


def generate_unlock_df(token_issue_date, total_token):

    df = initial_df(token_issue_date)

    # Define the total values
    stake_drops_total = int(total_token * 20 / 100)
    future_community_incentives_total = int(total_token * 15 / 100)
    rnd_ecosystem_total = int(total_token * 15 / 100)
    investor_total = int(total_token * 30 / 100)
    early_contributors_total = int(total_token * 20 / 100)
    total_unlock_total = total_token
    cumulative_total = total_token

    df["Stake Drops"] = df.apply(
        calculate_stake_drops,
        token_issue_date=token_issue_date,
        stake_drops_total=stake_drops_total,
        axis=1,
    )

    df["Future Community Incentives"] = df.apply(
        calculate_future_community_incentives,
        token_issue_date=token_issue_date,
        future_community_incentives_total=future_community_incentives_total,
        axis=1,
    )

    df["R&D Ecosystem"] = int(rnd_ecosystem_total / 48)

    df["Investor"] = df.apply(
        calculate_investor,
        token_issue_date=token_issue_date,
        investor_total=investor_total,
        axis=1,
    )

    df["Early Contributors"] = df.apply(
        calculate_early_contributors,
        token_issue_date=token_issue_date,
        early_contributors_total=early_contributors_total,
        axis=1,
    )

    df["Total Unlock"] = df.iloc[:, 1:].sum(axis=1)
    df["Cumulative"] = df["Total Unlock"].cumsum()
    df["Percentage"] = [
        f"{value * 100 :.2f}%" for value in df["Cumulative"] / cumulative_total
    ]

    # Create and concate the total row to the first row of df
    total_row = {
        "Date": ["Total"],
        "Stake Drops": [stake_drops_total],
        "Future Community Incentives": [future_community_incentives_total],
        "R&D Ecosystem": [rnd_ecosystem_total],
        "Investor": [investor_total],
        "Early Contributors": [early_contributors_total],
        "Total Unlock": [total_unlock_total],
        "Cumulative": [cumulative_total],
        "Percentage": ["100%"],
    }

    unlock_df = pd.concat([pd.DataFrame(total_row), df], ignore_index=True)
    return unlock_df
