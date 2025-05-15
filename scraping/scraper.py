import requests
from config.config import JOB_SEARCH_URL, HEADERS


class Scraper(object):
    def __init__(self, url=JOB_SEARCH_URL, headers=HEADERS):
        self.url = url
        self.headers = headers

    def single_page(self):
        response = requests.get(self.url, headers=self.headers)
        return response.text
