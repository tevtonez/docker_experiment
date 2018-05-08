"""Main views."""

from flask import (
    Flask,
)
from scrapyd_api import ScrapydAPI
from selenium import webdriver
from subprocess import Popen, PIPE

import os

app = Flask(__name__)

# p = Popen('docker exec -di 6800:6800 my_flask_app bash -c "cd tutorial/  && scrapyd"', stdin=PIPE)

scrapyd = ScrapydAPI('http://localhost:6800')

# prod = os.environ.get('PROD', None)
# if prod:
#     # getting port from heroku
#     port = int(os.environ.get('PORT', 17995))
#     print(int(os.environ.get('PORT', 17995)))
#     print('https://scrptest.herokuapp.com:{}'.format(str(port)))

#     scrapyd = ScrapydAPI('https://scrptest.herokuapp.com:{}'.format(str(port)))
#     # scrapyd = ScrapydAPI('http://localhost:6800')
# else:
#     scrapyd = ScrapydAPI('http://localhost:6800')


@app.route('/')
def index():
    """Index view."""
    return "Yes, it's working!"


@app.route('/selen')
def selen():
    """Selenium launcher."""
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "excludeSwitches",
        ["ignore-certificate-errors"]
    )
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')

    chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
    if chrome_bin:
        options.binary_location = chrome_bin
        driver = webdriver.Chrome(
            executable_path='chromedriver',
            options=options
        )

    driver = webdriver.Chrome(options=options)

    driver.get('http://octogear.com')

    return driver.page_source


@app.route('/scr')
def scrap():

    url = 'http://quotes.toscrape.com/page/1/'

    settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }

    task = scrapyd.schedule(
        'default',
        'quotes',
        settings=settings,
        url=url
    )

    return 'Task has been passed to scrapyd'

if __name__ == "__main__":
    app.run()
