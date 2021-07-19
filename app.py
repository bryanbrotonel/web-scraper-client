# NOTE: source venv/bin/activate; FLASK_ENV=development flask run

from flask import Flask, render_template, request
from urllib.parse import quote
import requests
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():

    return render_template('search.html',)


@app.route("/", methods=['POST'])
def results():

    search = request.form['search']

    searchArgs = quote(search)

    dfCraigslist = scarpe_craigslist(searchArgs)
    dfAmazon = scrape_amazon(searchArgs)
    dfEbay = scrape_ebay(searchArgs)

    df = dfCraigslist.append(dfAmazon).append(dfEbay)

    return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

def scrape_ebay(search):
    request = requests.get(
        'https://webscraper-server.herokuapp.com/crawl.json?spider_name=ebay&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D').json()
    return pd.DataFrame(request['items'])


def scarpe_craigslist(search):
    request = requests.get(
        'https://webscraper-server.herokuapp.com/crawl.json?spider_name=craigslist&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D').json()
    return pd.DataFrame(request['items'])


def scrape_amazon(search):
    request = requests.get(
        'https://webscraper-server.herokuapp.com/crawl.json?spider_name=amazon&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D').json()
    return pd.DataFrame(request['items'])


if __name__ == "__main__":
    app.run()
