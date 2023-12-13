# app.py (Flask application)

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_country_info(country_name):
    api_url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        if data:
            country_info = {
                'name': data[0]['name']['common'],
                'population': "{:,}".format(data[0]['population']),
                'capital': data[0]['capital'][0],
                'subregion': data[0]['subregion'],
                'area':  "{:,}".format(data[0]['area']),
                'currencies': ', '.join(data[0]['currencies'].keys()),
                'languages': ', '.join(data[0]['languages'].keys()),
                'flag_url': data[0]['flags']['png'],  # Assuming your data source provides a 'flags' field with PNG URL
            }

            return country_info

    return None

@app.route('/')
def index():
    return render_template('index.html', country_info=None)

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form.get('user_input')
    country_info = get_country_info(user_input)

    return render_template('index.html', country_info=country_info)


if __name__ == '__main__':
    app.run(debug=True)
