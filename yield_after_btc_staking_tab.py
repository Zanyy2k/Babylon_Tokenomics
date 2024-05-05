from helper_functions import initial_df


def generate_yield_after_btc_staking_df(
    token_issue_date,
    supply_df,
    annual_bbn_reward,
    token_price,
    annual_node_cost,
    no_of_nodes,
    amt_of_btc_staked,
    btc_cost,
    threshold,
):

    df = initial_df(token_issue_date)

    for i in range(5, 105, 5):

        # Initialize a list to store values for the current i
        values_for_i = []

        for d in df["Date"]:

            # Get the corresponding value from supply_df
            supply_value = supply_df.set_index("Date").loc[d, "Circulating Supply"]

            if threshold > 0.0:
                if i == 70:
                    temp_value = (
                        (
                            annual_bbn_reward * token_price
                            - (annual_node_cost * no_of_nodes)
                        )
                        / (i / 100 * supply_value * token_price)
                        / (
                            1
                            + min(
                                amt_of_btc_staked
                                * btc_cost
                                / (i / 100 * supply_value * token_price),
                                threshold,
                            )
                        )
                        * 100
                    )
            else:
                # Calculate the desired value based on the current i
                temp_value = (
                    (annual_bbn_reward * token_price - (annual_node_cost * no_of_nodes))
                    / (
                        i / 100 * supply_value * token_price
                        + (amt_of_btc_staked * btc_cost)
                    )
                    * 100
                )

            if i == 100:
                # Calculate the desired value based on the current i
                temp_value = (
                    (annual_bbn_reward * token_price - (annual_node_cost * no_of_nodes))
                    / (
                        i / 100 * supply_value * token_price
                        + (amt_of_btc_staked * btc_cost)
                        + (amt_of_btc_staked * btc_cost)
                    )
                    * 100
                )

            # Format the temp_value to 2 decimal places with '$' in front
            formatted_value = f"{temp_value:.2f}%"

            # Append the formatted value to the list
            values_for_i.append(formatted_value)

        df[f"{i}%"] = values_for_i

    return df
