import streamlit as st
import plotly.graph_objects as go

from unlock_tab import generate_unlock_df
from supply_tab import generate_supply_df
from issuance_tab import generate_issuance_df
from yield_tab import generate_yield_df
from total_validator_earning_tab import generate_total_validator_earning_df
from yield_after_btc_staking_tab import generate_yield_after_btc_staking_df
from profitablity_tab import generate_profitability_df

st.title("Babyon Tokenomics Model")

# Issuance Calculation Section
with st.container(border=True):

    # create a sidebar with sliders for input parameters
    st.sidebar.markdown("## Tokenomics Parameter")

    # Define year range
    token_issue_date = st.sidebar.date_input("Enter the token issue date: ")

    # slider for Total Token
    total_token = st.sidebar.slider(
        "Total Token", min_value=0, max_value=21000000000, value=21000000000
    )

    # slider for Staking Percentage
    staking_pct = st.sidebar.slider("Staking %", min_value=0, max_value=100, value=70)

    # slider for Target Yield Percentage
    target_yield_pct = st.sidebar.slider(
        "Target Yield %", min_value=0, max_value=10, value=3
    )

    st.sidebar.divider()

    # calculate & display Annual Reward based on input parameters
    annual_reward = staking_pct * target_yield_pct / 100
    st.sidebar.write("Annual Reward : ", annual_reward, "%")

    # calculate & display Annual BBN Reward based on Total Token and Annual Reward
    annual_bbn_reward = total_token * annual_reward / 100
    st.sidebar.write("Annual BBN Reward : ", annual_bbn_reward)


# Block Reward Calculation Section
with st.container(border=True):

    st.sidebar.markdown("## Block Reward Calculation")

    # slider for Block Time in Minutes
    block_time = st.sidebar.slider(
        "Block Time (Mins)", min_value=0, max_value=60, value=5
    )

    # calculate Blocks per Day based on Block Time
    blocks_per_day = 24 * 60 * 60 / block_time
    st.sidebar.write("Blocks per Day : ", blocks_per_day)

    # calculate Daily Issuance based on Annual BBN Reward
    daily_issuance = annual_bbn_reward / 365.25
    st.sidebar.write("Daily Issuance : ", round(daily_issuance, 2))

    # calculate Rewards per Block
    reward_per_block = daily_issuance / blocks_per_day
    st.sidebar.write("Rewards per Block : ", round(reward_per_block, 2))

    # input for BBN Price
    bbn_price = st.sidebar.number_input("Please Enter the BBN Price : ", value=0.5)
    st.sidebar.write("BBN Price : $", bbn_price)

    # slider for number of public chains and transactions per public chain
    no_public_chain = st.sidebar.slider(
        "Number of Public Chain", min_value=0, max_value=20, value=1
    )
    no_transaction_per_pchain = st.sidebar.slider(
        "Number of Transaction per Public Chain",
        min_value=0,
        max_value=500000,
        value=100000,
    )

    # average transaction fees
    avg_transaction_fees = st.sidebar.number_input(
        "Please Enter the Average Transaction fees ($): ", value=1.00
    )
    st.sidebar.write("Average Transaction Fees : $", avg_transaction_fees)

    # number of validators per public chain
    no_validators_per_pchain = st.sidebar.slider(
        "Number of validators per Public Chain", min_value=0, max_value=150, value=100
    )

    # validator-related Inputs
    yearly_running_cost_single_validator = st.sidebar.slider(
        "Yearly Running Cost of A Single Validator ($)",
        min_value=0,
        max_value=20000,
        value=10000,
    )
    initial_investment = st.sidebar.slider(
        "Initial Investment ($)", min_value=0, max_value=300000, value=100000
    )

    # divider for better UI
    st.sidebar.divider()

    # input for Validator Emission Incentives Calculation

    unlock_df = generate_unlock_df(token_issue_date, total_token)
    unlock_cummulative_latest_month = unlock_df["Cumulative"][1]
    st.sidebar.write("Cummulative Unlock : ", unlock_cummulative_latest_month)

    # calculate & display validator emission incentives
    validator_emission_incentives = total_token * bbn_price * annual_reward / 100
    st.sidebar.write("Validator Emission Incentives : $", validator_emission_incentives)

    # calculate & display validator fee incentives
    validator_fee_incentives = (
        no_public_chain * no_transaction_per_pchain * avg_transaction_fees
    )
    st.sidebar.write("Validator Fee Incentives : $", validator_fee_incentives)

    # calculate & display validator running costs
    validator_running_costs = (
        no_public_chain
        * no_validators_per_pchain
        * yearly_running_cost_single_validator
    )
    st.sidebar.write("Validator Running Costs : $", validator_running_costs)

    # calculate & display total validator earnings
    total_validator_earning = (
        validator_emission_incentives
        + validator_fee_incentives
        - validator_running_costs
    ) / (unlock_cummulative_latest_month * staking_pct / 100 * bbn_price)
    st.sidebar.write(
        "Total Validator Earning : ", round(total_validator_earning * 100, 2), "%"
    )


# Assumptions
with st.container(border=True):
    st.markdown(
        """ 
    #### Assumptions ####
    - Babylon has 1 billion of total supply in the beginning. Every year 210 million BBN token will be issued to reward validators.
    - The price of BBN token is 0.5$. 
    - 70% of circulating supply of BBN tokens are staked.
    - 500 BTC are also staked among Babylon validators.
    - The price of BTC is 30000.
    - The reward that a BTC delegator earns and the reward that a BBN delegator earn are the same. """
    )


# Create tabs
(
    unlock_tab,
    supply_tab,
    issuance_tab,
    yield_tab,
    total_validator_earning_tab,
    yield_after_btc_staking_tab,
    profitability_tab,
) = st.tabs(
    [
        "Unlock",
        "Supply",
        "Issuance",
        "Yield",
        "Total Validator Earning",
        "Yield after BTC staking",
        "Profitability",
    ]
)

# Unlock Tab
with unlock_tab:
    st.header("Unlock")
    st.dataframe(unlock_df)

    # Exclude the 'Date' column from the list of y-columns
    y_columns = unlock_df.columns.difference(["Date"])
    fig = go.Figure()
    for column in y_columns:
        fig.add_trace(
            go.Scatter(
                x=unlock_df["Date"], y=unlock_df[column], mode="lines", name=column
            )
        )
    st.plotly_chart(fig)


# Supply Tab
with supply_tab:
    st.header("Supply")
    supply_df = generate_supply_df(
        token_issue_date, unlock_df, daily_issuance, total_token
    )
    st.dataframe(supply_df)

    # Exclude the 'Date' column from the list of y-columns
    y_columns = supply_df.columns.difference(["Date"])
    fig = go.Figure()
    for column in y_columns:
        fig.add_trace(
            go.Scatter(
                x=supply_df["Date"], y=supply_df[column], mode="lines", name=column
            )
        )
    st.plotly_chart(fig)


# Issuance Tab
with issuance_tab:
    st.header("Issuance")
    issuance_df = generate_issuance_df(token_issue_date, supply_df, annual_bbn_reward)
    st.dataframe(issuance_df)

    # Exclude the 'Date' column from the list of y-columns
    y_columns = issuance_df.columns.difference(["Date"])
    fig = go.Figure()
    for column in y_columns:
        fig.add_trace(
            go.Scatter(
                x=issuance_df["Date"], y=issuance_df[column], mode="lines", name=column
            )
        )
    st.plotly_chart(fig)


# Yield Tab
with yield_tab:
    st.header("Yield")
    yield_df = generate_yield_df(token_issue_date, supply_df, annual_bbn_reward)
    txt = "Percentage of supply staked"
    st.markdown(f"<p style='text-align:center'>{txt}</p>", unsafe_allow_html=True)
    st.dataframe(yield_df)

    # Exclude the 'Date' column from the list of y-columns
    y_columns = yield_df.columns.difference(["Date"])
    fig = go.Figure()
    for column in y_columns:
        fig.add_trace(
            go.Scatter(
                x=yield_df["Date"], y=yield_df[column], mode="lines", name=column
            )
        )
    st.plotly_chart(fig)


# Total Validator Earning Tab
with total_validator_earning_tab:
    st.header("Total Validator Earning")
    total_validator_earning_df = generate_total_validator_earning_df(
        token_issue_date,
        unlock_df,
        validator_emission_incentives,
        validator_fee_incentives,
        validator_running_costs,
        bbn_price,
        initial_investment,
    )
    txt = "Percentage of supply staked"
    st.markdown(f"<p style='text-align:center'>{txt}</p>", unsafe_allow_html=True)
    st.dataframe(total_validator_earning_df)

    # Exclude the 'Date' column from the list of y-columns
    y_columns = total_validator_earning_df.columns.difference(["Date"])
    fig = go.Figure()
    for column in y_columns:
        fig.add_trace(
            go.Scatter(
                x=total_validator_earning_df["Date"],
                y=total_validator_earning_df[column],
                mode="lines",
                name=column,
            )
        )
    st.plotly_chart(fig)


# Yield After BTC Staking Tab
with yield_after_btc_staking_tab:
    st.header("Yield after BTC staking")

    # input token_price
    token_price = st.number_input("Please Enter the Token Price : ", value=0.5)
    st.write("Token Price : $", token_price)

    # input annual_node_cost
    annual_node_cost = st.number_input(
        "Please Enter the Annual Node Cost : ", value=10000.0
    )
    st.write("Annual Node Cost : $", annual_node_cost)

    # input no_of_nodes
    no_of_nodes = st.number_input("Please Enter the Number of Nodes : ", value=100)
    st.write("Number of Nodes : ", no_of_nodes)

    # input amt_of_btc_staked
    amt_of_btc_staked = st.number_input(
        "Please Enter the Amount of BTC Staked : ", value=500.0
    )
    st.write("Amount of BTC staked : ", amt_of_btc_staked)

    # input btc cost
    btc_cost = st.number_input("Please Enter the Cost of BTC : ", value=30000.0)
    st.write("Cost of BTC : ", btc_cost)

    # input threshold. Default 0.0 for no threshold else threshold is active
    threshold = st.number_input(
        "Please Enter the Threshold (Default 0.0 for no threshold) : ", value=0.0
    )
    st.write("Threshold : ", threshold)

    yield_after_btc_staking_df = generate_yield_after_btc_staking_df(
        token_issue_date,
        supply_df,
        annual_bbn_reward,
        token_price,
        annual_node_cost,
        no_of_nodes,
        amt_of_btc_staked,
        btc_cost,
        threshold,
    )

    txt = "Percentage of supply staked"
    st.markdown(f"<p style='text-align:center'>{txt}</p>", unsafe_allow_html=True)
    st.dataframe(yield_after_btc_staking_df)

    # Exclude the 'Date' column from the list of y-columns
    y_columns = yield_after_btc_staking_df.columns.difference(["Date"])
    fig = go.Figure()
    for column in y_columns:
        fig.add_trace(
            go.Scatter(
                x=yield_after_btc_staking_df["Date"],
                y=yield_after_btc_staking_df[column],
                mode="lines",
                name=column,
            )
        )
    st.plotly_chart(fig)


# Profitability Tab
with profitability_tab:
    st.header("Profitability")

    # Define token price range
    start_token_price, end_token_price = st.select_slider(
        "Select the token price range: ",
        options=[
            0,
            0.5,
            1,
            1.5,
            2,
            2.5,
            3,
            3.5,
            4,
            4.5,
            5,
            5.5,
            6,
            6.5,
            7,
            7.5,
            8,
            8.5,
            9,
            9.5,
            10,
        ],
        value=(0.5, 6.5),
    )
    st.write(
        "You selected token price range between",
        start_token_price,
        "and",
        end_token_price,
    )

    commission_rate = st.slider(
        "Commission Rate : ", min_value=0, max_value=100, value=10
    )

    no_of_nodes = st.multiselect("Select number of nodes : ", [50, 100], [50, 100])

    annual_cost = st.multiselect(
        "Select Annual Cost ($) : ",
        [25000, 50000, 75000, 100000],
        [25000, 50000, 75000, 100000],
    )

    profitability_df = generate_profitability_df(
        start_token_price,
        end_token_price,
        commission_rate,
        no_of_nodes,
        annual_cost,
        annual_bbn_reward,
    )

    txt = "Annual profit per node:"
    st.markdown(f"<p style='text-align:center'>{txt}</p>", unsafe_allow_html=True)
    st.dataframe(profitability_df)

    y_columns = profitability_df.columns.difference(["Annual Cost", "Number of Nodes"])
    node_values = profitability_df["Number of Nodes"].unique()
    selected_node = st.selectbox("Select Number of Nodes", node_values)

    # Filter DataFrame based on the selected 'Number of Nodes'
    filtered_df = profitability_df[profitability_df["Number of Nodes"] == selected_node]

    # Create a subplot for each column in y_columns
    fig = go.Figure()
    for column in y_columns:
        fig.add_trace(
            go.Scatter(
                x=filtered_df["Annual Cost"],
                y=filtered_df[column],
                mode="lines",
                name=column,
            )
        )

    fig.update_layout(
        xaxis_title="Annual Cost", yaxis_title="Value", title="Profitability Analysis"
    )

    # Display the subplot in Streamlit
    st.plotly_chart(fig)
