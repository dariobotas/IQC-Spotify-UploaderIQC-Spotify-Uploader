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