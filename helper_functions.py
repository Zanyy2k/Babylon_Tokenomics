import pandas as pd
from datetime import timedelta


# def last_day_of_month(any_day):
#     next_month = any_day.replace(day=28) + timedelta(days=4)
#     return (next_month - timedelta(days=next_month.day)).date()


def generate_date_range(token_issue_date, num_years):
    start_date = pd.Timestamp(token_issue_date)
    end_date = start_date + pd.DateOffset(years=num_years)

    # Generate dates for each month
    date_range = []
    current_date = start_date
    while current_date < end_date:
        date_range.append(current_date.date())

        # Move to the next month
        current_date = current_date + pd.DateOffset(months=1)

        # Set the day to the token issue day
        current_date = current_date.replace(day=start_date.day)
    return date_range

    # date_range = pd.date_range(start_date, end_date, freq="M")
    # print("date_range : ", date_range)
    # last_days_of_month = [last_day_of_month(date) for date in date_range]
    # return last_days_of_month


def initial_df(token_issue_date):

    num_years = 4
    months_range = generate_date_range(token_issue_date, num_years)
    data = {"Date": months_range}
    initial_df = pd.DataFrame(data)
    # print(initial_df)
    return initial_df
