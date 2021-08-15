# NOTE: source venv/bin/activate; FLASK_ENV=development flask run

from flask import Flask, render_template, request
from urllib.parse import quote
import requests
import pandas as pd
from functools import partial
import multiprocessing

app = Flask(__name__)

@app.route("/")
def index():

    return render_template('search.html',)

@app.route("/", methods=['POST'])
def results():
    search = request.form['search']
    searchArgs = quote(search)

    column_names = ['Product Name', 'Product Author', 'Product Price', 'Product Image']
    df = pd.DataFrame(columns = column_names)

    websites = ['amazon', 'ebay', 'craigslist']

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = pool.map(partial(scrape_data, search=searchArgs), websites)

    return render_template('table.html',  tables=[df.append([data for data in results]).to_html(index=False)], titles=df.columns.values)

def scrape_data(website, search):
    return pd.DataFrame(requests.get('https://webscraper-server.herokuapp.com/crawl.json?spider_name=' + website + '&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D').json()['items'])

if __name__ == "__main__":
    app.run()