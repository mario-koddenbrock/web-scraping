import os
import time
import urllib.request
from datetime import date

import lxml
import requests
from bs4 import BeautifulSoup

html_folder_path = ".\\html-content"
html_files = os.listdir(html_folder_path)

for html in html_files:

    with open(f"{html_folder_path}\\{html}") as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    paragraphs = soup.findAll('p')

    for p in paragraphs:
        print(p.prettify)
