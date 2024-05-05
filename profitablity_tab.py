import pandas as pd 

def generate_profitability_df(start_token_price, end_token_price, commission_rate, no_of_nodes, annual_cost, annual_bbn_reward):

    # Create empty lists to store data
    token_prices_list = []
    annual_costs_list = []
    no_of_nodes_list = []
    annual_profit_value_list = []


    for token_price in range(int(start_token_price*10), int(end_token_price*10 + 5), 5):
        token_price = token_price / 10.0

        for ac in annual_cost:
            for node in no_of_nodes:
                annual_profit_value = annual_bbn_reward * token_price / node * commission_rate/100 - ac

                # Append values to the lists
                token_prices_list.append(f'${token_price:.1f}')
                annual_costs_list.append(ac)
                no_of_nodes_list.append(node)
                annual_profit_value_list.append(annual_profit_value)

    # Create a DataFrame from the lists
    df = pd.DataFrame({
        'Token Price': token_prices_list,
        'Annual Cost': annual_costs_list,
        'Number of Nodes': no_of_nodes_list,
        'Calculated Value': annual_profit_value_list
    })

    # Pivot the DataFrame
    df_pivot = df.pivot_table(index=['Number of Nodes', 'Annual Cost'], columns='Token Price', values='Calculated Value')

    # Reset index to make 'Number of Nodes' and 'Annual Cost' as columns
    df_pivot.reset_index(inplace=True)

    # Sort the DataFrame by 'Number of Nodes' and then 'Annual Cost'
    df_pivot.sort_values(by=['Number of Nodes', 'Annual Cost'], inplace=True)

    return df_pivot 

