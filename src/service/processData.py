import pandas as pd
import readJason  # Import the readJason module


# Return dataframe from read_json as dataframe
def get_data():
    # Get the dataframe from the read_json file
    df = readJason.read_json()

    # Return the dataframe
    return df


def calculate_total_tests(date):
    # Convert the input date to datetime
    date = pd.to_datetime(date)

    # Get the dataframe
    df = get_data()

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Filter the dataframe to include only rows where the 'date' column is less than the provided date
    df = df[df['date'] < date]

    # Convert the 'total_results_reported' column to numeric
    df['total_results_reported'] = pd.to_numeric(df['total_results_reported'])

    # Calculate the total number of tests performed
    total_tests = df['total_results_reported'].sum()

    return total_tests



