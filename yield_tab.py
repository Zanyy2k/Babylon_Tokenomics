from helper_functions import initial_df


def generate_yield_df(token_issue_date, supply_df, annual_bbn_reward):

    df = initial_df(token_issue_date)

    for i in range(5, 105, 5):

        # Initialize a list to store values for the current i
        values_for_i = []

        for d in df["Date"]:

            # Get the corresponding value from supply_df
            supply_value = supply_df.set_index("Date").loc[d, "Circulating Supply"]

            # Calculate the desired value based on the current i
            temp_value = annual_bbn_reward / (i / 100 * supply_value) * 100

            # Format the temp_value to 2 decimal places with '%' at the end
            formatted_value = f"{temp_value:.2f}%"

            # Append the result to the list
            values_for_i.append(formatted_value)

        df[f"{i}%"] = values_for_i

    return df
