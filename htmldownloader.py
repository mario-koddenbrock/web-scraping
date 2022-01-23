import os
import time
import urllib.request
from datetime import date

import lxml
import requests
from bs4 import BeautifulSoup


class HtmlDownloader:

    def __init__(self,
                 rss_path="https://www.tagesschau.de/xml/rss2/",
                 html_folder="html-content",
                 waiting_seconds=600):

        self.rss_path = rss_path
        self.html_folder = html_folder
        self.waiting_seconds = waiting_seconds

        if os.path.isdir(self.html_folder):
            try:
                os.mkdir(self.html_folder)
            except OSError:
                print(f"Creation of the directory for html content failed [{self.html_folder}]")

        print(f"Initialize downloadin loop: {self.rss_path}")

    def run(self):
        while True:

            self.download_new_articles()
            time.sleep(self.waiting_seconds)

    def download_new_articles(self):

        rss_soup = self.get_rss_soup()
        articles = rss_soup.findAll('item')
        count_new_article = 0

        for a in articles:
            title = a.find('title').text
            link = a.find('guid').text
            name = os.path.basename(link)
            local_html_path = f"{self.html_folder}\\{name}"

            if os.path.isfile(local_html_path):
                continue

            count_new_article += 1
            print(f"Found new Article: {title} \n -> saved to {local_html_path}")

            urllib.request.urlretrieve(link,
                                       local_html_path)

        print(f"[{date.today()}] Found {count_new_article} new articles")

    def get_rss_soup(self):
        try:
            r = requests.get(self.rss_path)
            soup = BeautifulSoup(r.content, features='lxml')
            return soup
        except Exception as e:
            raise e
