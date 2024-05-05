from helper_functions import initial_df


def generate_issuance_df(token_issue_date, supply_df, annual_bbn_reward):

    df = initial_df(token_issue_date)

    df["Relative Issuance"] = [
        f"{annual_bbn_reward / value * 100 :.2f}%"
        for value in supply_df.set_index("Date")
        .loc[df["Date"], "Circulating Supply"]
        .values
    ]
    df["Absolute Issuance"] = [
        f"{annual_bbn_reward / value * 100 :.2f}%"
        for value in supply_df.set_index("Date").loc[df["Date"], "Total Supply"].values
    ]

    return df
