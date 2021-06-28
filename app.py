from flask import Flask, render_template
import requests
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
  return "Web Scraper Client"

if __name__ == "__main__":
  app.run()
