# this file loads the json file and adds the values to the object.

import requests
import pandas as pd
import os


# Open the JSON file
def read_json():
    # Define the directory and file path
    directory = "../json"
    file_name = "pcr_testing_data_download.json"
    file_path = os.path.join(directory, file_name)

    # Read the JSON file into a DataFrame
    df = pd.read_json(file_path)

    # Return the DataFrame
    # print(df)
    return df


# read_json()
