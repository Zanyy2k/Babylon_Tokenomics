from helper_functions import initial_df


def generate_total_validator_earning_df(
    token_issue_date,
    unlock_df,
    validator_emission_incentives,
    validator_fee_incentives,
    validator_running_costs,
    bbn_price,
    initial_investment,
):

    df = initial_df(token_issue_date)

    for i in range(10, 110, 10):

        # Initialize a list to store values for the current i
        values_for_i = []

        for d in df["Date"]:

            # Get the corresponding value from unlock_df
            unlock_cumulative_value = unlock_df.set_index("Date").loc[d, "Cumulative"]

            # Calculate the desired value based on the current i
            temp_value = (
                (
                    validator_emission_incentives
                    + validator_fee_incentives
                    - validator_running_costs
                )
                / (unlock_cumulative_value * bbn_price * i / 100)
                * initial_investment
            )

            # Format the temp_value to 2 decimal places with '$' in front
            formatted_value = f"${temp_value:.2f}"

            # Append the formatted value to the list
            values_for_i.append(formatted_value)

        df[f"{i}%"] = values_for_i
    return df
