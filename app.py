# NOTE: source venv/bin/activate; FLASK_ENV=development flask run

from flask import Flask, render_template, request
from urllib.parse import quote
import requests
import pandas as pd
from functools import partial
import multiprocessing
import json

app = Flask(__name__)

@app.route("/")
def index():

    return render_template('search.html',)

@app.route("/", methods=['POST'])
def results():
    search = request.form['search']
    searchArgs = quote(search)

    websites = ['craigslist', 'ebay', 'amazon']
    items = []

    pool = multiprocessing.Pool(processes=3)
    results = pool.map(partial(scrape_data, search=searchArgs), websites)

    for data in results:
        items += data['items']

    newlist = sorted(items, key=lambda k: k['Product Name']) 

    return render_template('table.html',  data=newlist, search=search)

def scrape_data(website, search):
    return requests.get('https://webscraper-server.herokuapp.com/crawl.json?spider_name=' + website + '&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D').json()

if __name__ == "__main__":
    app.run()