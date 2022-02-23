import os
import time
import urllib.request
from datetime import datetime

import lxml
import requests
from bs4 import BeautifulSoup

from web_scraping.notification import send_mail


class HtmlDownloader:

    def __init__(self,
                 rss_path="https://www.tagesschau.de/xml/rss2/",
                 html_folder="html-content",
                 waiting_seconds=600):

        self.rss_path = rss_path
        self.html_folder = html_folder
        self.waiting_seconds = waiting_seconds
        
        if not os.path.isdir(self.html_folder):
            try:
                os.mkdir(self.html_folder)
            except OSError:
                print(f"Creation of the directory for html content failed [{self.html_folder}]")

        print(f"Initialize downloading: {self.rss_path}")

    def __del__(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_mail("Python Script Stopped", now)

    def run(self):
        while True:

            self.download_articles_html()

            for sec in range(self.waiting_seconds, 0, -1):
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\r[{now}] Still waiting {sec} seconds...", end='')
                time.sleep(1)

            print(f"\r[{datetime.now()}] Starting again...")

    def download_articles_rss(self):

        rss_soup = self.get_rss_soup()
        articles = rss_soup.findAll('item')
        count_new_article = 0

        for a in articles:
            # title = a.find('title').text
            link = a.find('guid').text
            name = os.path.basename(link)
            
            
            local_html_path = os.path.join(self.html_folder, name)
            # local_html_path = f"{self.html_folder}\\{name}"

            if os.path.isfile(local_html_path):
                continue

            count_new_article += 1
            print(f"Found new Article: {local_html_path}")

            urllib.request.urlretrieve(link,
                                       local_html_path)

        if (count_new_article > 0):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] Found {count_new_article} new articles (from {len(articles)})")

    def download_articles_html(self):

        r = requests.get("https://www.tagesschau.de")
        soup = BeautifulSoup(r.content, 'html.parser')

        divs = soup.findAll('a', {"class": "teaser__link"}, href=True)
        count_article_new = 0
        count_articles = 0

        for div in divs:

            link = div["href"]

            if not link.endswith(".html"):
                continue

            name = os.path.basename(link)
            local_html_path = os.path.join(self.html_folder, name)
            # local_html_path = f"{self.html_folder}\\{name}"
            count_articles += 1

            if os.path.isfile(local_html_path):
                continue

            count_article_new += 1
            print(f"Found new Article: {local_html_path}")

            urllib.request.urlretrieve(link, local_html_path)

        if (count_article_new > 0):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] Found {count_article_new} new articles (from {count_articles})")

    def get_rss_soup(self):
        try:
            r = requests.get(self.rss_path)
            soup = BeautifulSoup(r.content, features='lxml')
            return soup
        except Exception as e:
            raise e
