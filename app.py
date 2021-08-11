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

    dfCraigslist = scarpe_craigslist(searchArgs)
    dfAmazon = scrape_amazon(searchArgs)
    dfEbay = scrape_ebay(searchArgs)

    df = dfCraigslist.append(dfAmazon).append(dfEbay)

    return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

def scrape_ebay(search):
    ebayLink = 'https://webscraper-server.herokuapp.com/crawl.json?spider_name=ebay&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D'

    print(ebayLink, file=sys.stderr)
    print(ebayLink, file=sys.stdout)

    request = requests.get(ebayLink).json()
    return pd.DataFrame(request['items'])


def scarpe_craigslist(search):
    craigslistLink = 'https://webscraper-server.herokuapp.com/crawl.json?spider_name=craigslist&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D'

    print(craigslistLink, file=sys.stderr)
    print(craigslistLink, file=sys.stdout)

    request = requests.get(craigslistLink).json()
    return pd.DataFrame(request['items'])


def scrape_amazon(search):
    amazonLink = 'https://webscraper-server.herokuapp.com/crawl.json?spider_name=amazon&start_requests=true&crawl_args=%7B%22search%22%3A%20%22' + search + '%22%7D'

    print(amazonLink, file=sys.stderr)
    print(amazonLink, file=sys.stdout)

    request = requests.get(amazonLink).json()
    return pd.DataFrame(request['items'])


if __name__ == "__main__":
    app.run()