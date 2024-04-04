import json
import time
from enum import Enum
from pytube import YouTube
from sys import platform

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchWindowException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains


class ContentType(Enum):
    MESSAGE = "Mensagem"
    BIBLE_STUDY = "Estudo Bíblico"


class SpotifyChannel:
    def __init__(self, channel_url):
        self.channel_url = channel_url
        self.file_title = ""
        self.description = ""
        self.content_type = ContentType
        self.publication_date = ""
        self.explicit_content = False
        self.promotional_content = False
        self.season = 1
        self.episode = 0

    @property
    def file_title(self):
        return self.file_title

    @file_title.setter
    def file_title(self, value):
        self._file_title = value

    @property
    def description(self):
        return self.description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def content_type(self):
        return self.content_type

    @content_type.setter
    def content_type(self, value: ContentType):
        self._content_type = value

    @property
    def publication_date(self):
        return self.publication_date

    @publication_date.setter
    def publication_date(self, value):
        self._publication_date = value

    def access_spotify(self):
        driver_service = ""
        options = Options()
        #options.add_argument("--headless")

        if platform == "linux" or platform == "linux2":
            driver_service = Service(r'/snap/bin/geckodriver')  # for linux systems
        elif platform == "win32" or platform == "win64":
            driver_service = Service()  # for Windows systems

        driver = webdriver.Edge(service=driver_service,
                                options=options)  # Update this with the path to your webdriver executable
        try:
            driver.get(self.channel_url)
        except TimeoutError as timeout_error:
            print(f"Timeout error: {timeout_error}")
        except TimeoutException as time_out_exception:
            print(f"{time_out_exception}\nURL: {self.channel_url}\n")
        except NoSuchWindowException as window_exception:
            print(f"{window_exception}URL: {self.channel_url}\n")
        except WebDriverException as webdriver_exception:
            print(f"{webdriver_exception}URL: {self.channel_url}\n")
        else:
            if "404" in driver.title:
                driver.close()
                return "404"


