import requests
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)


@app.route('/get-data', methods=['GET'])
def get_data():
    limit = 1000
    offset = 0
    data = []

    while True:
        response = requests.get(f'https://healthdata.gov/resource/j8mb-icvb.json?$limit={limit}&$offset={offset}')
        response_data = response.json()
        if not response_data:
            break
        data.extend(response_data)
        offset += limit

    print(jsonify(data))
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True)
