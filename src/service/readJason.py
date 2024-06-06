# this file loads the json file and adds the values to the object.

import json
import pandas as pd

# Open the JSON file
with open("../json/j8mb-icvb.json", "r") as f:
    data = json.load(f)

# # Iterate over each dictionary in the list
# for dictionary in data:
#     # Print the items of each dictionary
#     print(dictionary.items())


# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)

# Print the DataFrame
print(df)