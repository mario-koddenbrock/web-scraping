import os
import time
import urllib.request
from datetime import datetime

import lxml
import requests
from bs4 import BeautifulSoup
from notification import send_mail


class HtmlDownloadMonitoring:

    def __init__(self,
                 html_folder="html-content",
                 time_threshold=6,
                 waiting_seconds=600):

        self.html_folder = html_folder
        self.time_threshold = time_threshold  # in hours
        self.waiting_seconds = waiting_seconds

        if not os.path.isdir(self.html_folder):
            # todo need an small advice from chris here!
            send_mail(**self.format_mail_content("Folder not found!", "HTML Folder missing"))

    def format_mail_content(self, subject, content):

        subject_str = f"Project DataScience 22: {subject}"
        content_str = f"""Hi there!\n\n
                        We have a problem with our small webserver\n
                        Something is going wrong here. Someone please check on me.\n\n
                        ERROR:\n
                        {content}"""

        return (subject_str, content_str)


monitor = HtmlDownloadMonitoring(html_folder="dummy")
