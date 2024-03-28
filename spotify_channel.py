import json
import time
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


class SpotifyChannel:
    def __init__(self, channel_url):
        self.channel_url = channel_url
        self.file_title = ""

