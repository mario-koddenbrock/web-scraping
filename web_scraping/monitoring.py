# %%
import os
import time
from datetime import datetime, timedelta
from os import walk

from web_scraping.notification import send_mail


class HtmlDownloadMonitoring:

    def __init__(self,
                 html_folder="html-content",
                 time_threshold=6,
                 waiting_seconds=600):

        self.html_folder = html_folder
        self.time_threshold = timedelta(hours=time_threshold)  # in hours
        self.waiting_seconds = waiting_seconds

        if not os.path.isdir(self.html_folder):
            # todo: need an small advice from chris here!
            send_mail(**self.format_mail_content("Folder not found!", "HTML Folder missing"))

    def run(self):

        while True:

            if not self.check_files():
                text = f"""No new articles have been downloaded in the last 
                        {self.time_threshold} hours, maybe something is wrong 
                        with the web server."""
                send_mail(**self.format_mail_content("No new files!", text))
                return

            for sec in range(self.waiting_seconds, 0, -1):
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\r[{now}] Still waiting {sec} seconds...", end='')
                time.sleep(1)

    def check_files(self):
        filenames = next(walk(self.html_folder), (None, None, []))[2]

        for file in filenames:
            created = datetime.fromtimestamp(os.path.getctime(
                f"{self.html_folder}\\{file}"))

            time_delta = datetime.now() - created

            if (time_delta < self.time_threshold):
                return True

        return False

    def format_mail_content(self, subject, content):

        subject_str = f"Project DataScience 22: {subject}"
        content_str = f"""Hi there!\n\n
                        We have a problem with our small webserver\n
                        Something is going wrong here. Someone please check on me.\n\n
                        ERROR:\n
                        {content}"""

        return (subject_str, content_str)


monitor = HtmlDownloadMonitoring(html_folder="html-content")
monitor.run()
