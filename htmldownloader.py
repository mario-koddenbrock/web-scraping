import os
import urllib.request

import lxml
import requests
from bs4 import BeautifulSoup


class HtmlDownloader:

    def __init__(self, rss_path="https://www.tagesschau.de/xml/rss2/"):
        self.rss_path = rss_path

    def run(self):

        rss_soup = self.get_rss_soup()
        articles = rss_soup.findAll('item')

        for a in articles:
            title = a.find('title').text
            link = a.find('guid').text
            name = os.path.basename(link)
            local_html_path = f"html-content\\{name}"

            if os.path.isfile(local_html_path):
                continue

            print(f"Found new Article: {title} \n -> saved to {local_html_path}")

            urllib.request.urlretrieve(link,
                                       local_html_path)

    def get_rss_soup(self):
        try:
            r = requests.get(self.rss_path)
            soup = BeautifulSoup(r.content, features='lxml')
            return soup
        except Exception as e:
            raise e
