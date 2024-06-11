import pandas as pd
from src.service import read_json_data  # Import the readJason module
from datetime import datetime, timedelta


# Return dataframe from read_json as dataframe
def get_file_data():
    # Get the dataframe from the read_json file
    df = read_json_data.read_json()

    # Return the dataframe
    return df


def calculate_total_tests(date):
    # Convert the input date to datetime
    date = pd.to_datetime(date)

    # Get the dataframe
    df = get_file_data()

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Filter the dataframe to include only rows where the 'date' column is less than the provided date
    df = df[df['date'] < date]

    # Convert the 'total_results_reported' column to numeric
    df['total_results_reported'] = pd.to_numeric(df['total_results_reported'])

    # Calculate the total number of tests performed
    total_tests = df['total_results_reported'].sum()

    # print(total_tests)
    return total_tests


# calculate_total_tests('2020-06-01')


def calculate_rolling_average(date):
    # Convert the input date to datetime
    date = pd.to_datetime(date)

    # Get the dataframe
    df = get_file_data()

    # Convert the 'new_results_reported' column to numeric
    df['new_results_reported'] = pd.to_numeric(df['new_results_reported'])

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Calculate the date 30 days before the provided date
    thirty_days_ago = date - timedelta(days=30)

    # Filter the dataframe to include only rows where the 'date' column is within the range
    df = df[(df['date'] >= thirty_days_ago) & (df['date'] <= date)]

    # Calculate the 7-day rolling average of the 'new_results_reported' column
    df['7_day_average'] = df['new_results_reported'].rolling(window=7, min_periods=7).mean()

    # Select only the 'state', 'total_results_reported', 'date', and '7_day_average' columns
    df = df[['state', 'total_results_reported', 'date', '7_day_average']]

    # Get the last value of the '7_day_average' column
    # print(df.loc[:, ['date', '7_day_average']])  # print the date and 7_day_average columns
    #
    # # Plot the '7_day_average' column
    # df.plot.line(x='date', y='7_day_average')
    # plt.show()
    # return df.loc[:, ['date', '7_day_average']]  # return the date and 7_day_average columns

    return df


# calculate_rolling_average('2020-06-01')


def calculate_positivity_rate(date):
    # Convert the input date to datetime
    date = pd.to_datetime(date)

    # Get the dataframe
    df = get_file_data()

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Calculate the date 30 days before the provided date
    thirty_days_ago = date - timedelta(days=30)

    # Filter the dataframe to include only rows where the 'date' column is within the range
    df = df[(df['date'] >= thirty_days_ago) & (df['date'] <= date)]

    # Convert the 'new_results_reported' and 'total_results_reported' columns to numeric
    df['new_results_reported'] = pd.to_numeric(df['new_results_reported'])
    df['total_results_reported'] = pd.to_numeric(df['total_results_reported'])

    # Group the dataframe by 'state' and calculate the sum of 'new_results_reported' and 'total_results_reported' for
    # each state
    df_grouped = df.groupby('state')[['new_results_reported', 'total_results_reported']].sum()

    # Calculate the test positivity rate for each state
    df_grouped['positivity_rate'] = df_grouped['new_results_reported'] / df_grouped['total_results_reported']

    # Sort the dataframe by the test positivity rate in descending order and get the top 10 states
    top_10_states = df_grouped.sort_values(by='positivity_rate', ascending=False).head(10)

    # Reset the index of the DataFrame to include the state names in the output
    top_10_states.reset_index(inplace=True)

    # print(top_10_states)
    return top_10_states


# calculate_positivity_rate('2020-08-01')
