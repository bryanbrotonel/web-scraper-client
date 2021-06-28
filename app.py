from flask import Flask, render_template
import requests
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():

  return "/amazon for Amazon Spider<br>/craigslist for Craigslist Spider<br>/ebay for Ebay Spider"

@app.route("/ebay")
def ebay():

  arg = 'search'
  argValue = 'Nintendo Switch Console'

  request = requests.get(
      'https://webscraper-server.herokuapp.com/crawl.json?spider_name=ebay&start_requests=True&crawl_args=%7B%22' + arg + '%22%3A%20' + argValue + '%7D').json()
  df = pd.DataFrame(request['items'])

  return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

@app.route("/craigslist")
def craigslist():

  request = requests.get(
      'https://webscraper-server.herokuapp.com/crawl.json?spider_name=craigslist&url=https://vancouver.craigslist.org/d/for-sale/search/sss?query=nintendo%20switch%20console&sort=rel').json()
  df = pd.DataFrame(request['items'])

  return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

@app.route("/amazon")
def amazon():

  request = requests.get(
      'https://webscraper-server.herokuapp.com/crawl.json?spider_name=amazon&url=https://www.amazon.ca/Books-Last-30-days/s?rh=n%3A916520%2Cp_n_date%3A12035756011').json()
  df = pd.DataFrame(request['items'])

  return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

if __name__ == "__main__":
  app.run()
