from flask import Flask, render_template
import requests
from scrapinghub import ScrapinghubClient
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
  response = requests.get(
      'http://localhost:16210/crawl.json?spider_name=quotes&url=http://quotes.toscrape.com/').json()['items']
  df = pd.DataFrame(data=response)

  return render_template('table.html',  tables=[df.to_html(index=False)], titles=df.columns.values)

if __name__ == "__main__":
  app.run()
