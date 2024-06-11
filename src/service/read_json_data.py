import pandas as pd
import os


# Open the JSON file
def read_json():
    # Get the absolute path of the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the file path
    file_path = os.path.join(script_dir, "../../src/json/pcr_testing_data_download.json")

    # Read the JSON file into a DataFrame
    df = pd.read_json(file_path)

    # Return the DataFrame
    # print(df)
    return df


# read_json()
