import requests
from flask import Flask, jsonify
import json
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "The local server is ready!", 200


@app.route('/get-data', methods=['GET'])
def get_data():
    limit = 1000
    offset = 0
    data = []

    try:
        while True:
            response = requests.get(f'https://healthdata.gov/resource/j8mb-icvb.json?$limit={limit}&$offset={offset}')
            response_data = response.json()
            if not response_data:
                break

            # Process the data in smaller chunks here
            for item in response_data:
                # Process each item here
                # print(item)
                data.append(item)

            offset += limit
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data", "message": str(e)}), 500

    # Define the directory and file path
    directory = "../json"
    file_name = "pcr_testing_data_download.json"
    file_path = os.path.join(directory, file_name)

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Write the data to the file
    with open(file_path, 'w') as f:
        json.dump(data, f)

    return json.dumps({"message": "Data saved successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')