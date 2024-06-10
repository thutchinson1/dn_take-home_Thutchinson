# this file loads the json file and adds the values to the object.

import requests
import pandas as pd


# Open the JSON file
def read_json():
    # Send a GET request to the /get-data endpoint
    response = requests.get('http://localhost:5000/get-data')

    # Get the JSON data from the response
    data = response.json()

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Return the DataFrame
#     print(df)
    return df


# read_json()
