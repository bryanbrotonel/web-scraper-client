# NOTE: source venv/bin/activate; FLASK_ENV=development flask run

from flask import Flask, render_template, request
from urllib.parse import quote
import requests
import pandas as pd
import sys

app = Flask(__name__)


@app.route("/")
def index():

    return render_template('search.html',)


@app.route("/", methods=['POST'])
def results():

    search = request.form['search']

    searchArgs = quote(search)

    # dfCraigslist = scarpe_craigslist(searchArgs)
    # dfAmazon = scrape_amazon(searchArgs)
    # dfEbay = scrape_ebay(searchArgs)

    df = scarpe_craigslist(searchArgs).append(scrape_amazon(searchArgs)).append(scrape_ebay(searchArgs))

    return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

def scrape_ebay(search):
    ebayLink = 'https://webscraper-server.herokuapp.com/crawl.json?spider_name=ebay&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D'

    for i in range(3):
        attempts = i
        while True :
            try:
                request = requests.get(ebayLink).json()
            except requests.exceptions.Timeout:
                attempts-=1
                continue
            break
    return pd.DataFrame(request['items'])


def scarpe_craigslist(search):
    craigslistLink = 'https://webscraper-server.herokuapp.com/crawl.json?spider_name=craigslist&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D'

    for i in range(3):
        attempts = i
        while True :
            try:
                request = requests.get(craigslistLink).json()
            except requests.exceptions.Timeout:
                attempts-=1
                continue
            break

    return pd.DataFrame(request['items'])


def scrape_amazon(search):
    amazonLink = 'https://webscraper-server.herokuapp.com/crawl.json?spider_name=amazon&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D'

    for i in range(3):
        attempts = i
        while True :
            try:
                request = requests.get(amazonLink).json()
            except requests.exceptions.Timeout:
                attempts-=1
                continue
            break

    return pd.DataFrame(request['items'])


if __name__ == "__main__":
    app.run()