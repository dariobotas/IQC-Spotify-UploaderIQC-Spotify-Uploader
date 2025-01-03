import json
import time
from enum import Enum
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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec



class ContentType(Enum):
    MESSAGE = "Mensagem"
    BIBLE_STUDY = "Estudo Bíblico"


class SpotifyChannel:
    _xpath_login_h1 = "//h1[contains(@class, 'Type__TypeElement-sc-goli3j-0')]"
    _xpath_onetrust_policy_title = "//*[@id=\"onetrust-policy-title\"]"
    _xpath_onetrust_policy_button_permit = "//button[@id=\"onetrust-accept-btn-handler\" and text()=\"Permitir tudo\"]"
    _xpath_continuar_com_spotify_button = "//button[contains(@class, 'Button-sc-qlcn5g-0')]"
    _xpath_iniciar_sessao_title: str = "//h1[contains(@class, 'sc-bqWxrE gmSfcE')]"
    _xpath_username_input = "//input[@id='login-username']"
    _xpath_password_input = "//input[@id='login-password']"
    _xpath_login_button = "//button[@id='login-button']"
    _xpath_confirmation_identity_button = "//button[contains(@class, 'Button-sc-qlcn5g-0')]"
    _xpath_dashboard_title = "//*[@id='app-content']/div/div/div[1]/header/div[2]/div[1]/h1/div"
    # Dashboard content
    _xpath_novo_episodio_a_button = ("//*[@id=\"__chrome\"]//chrome-app/div/nav/div/div/dl/dt[1]/a["
                                     "@class='Button-sc-qlcn5g-0 cqSMED' and @aria-label='Criar um novo "
                                     "episódio')]//span[contains(text(), 'Novo episódio')]")
    _xpath_inicio_a_button = ("//*[@id=\"__chrome\"]//chrome-app/div/nav/div/div/dl/dd[1]/a[aria-label='Início' and "
                              "class='Link-sc-7welv8-1 gefhdY styles__StyledNavigationListItem-sc-1c80vy6-11 dsQriY']")
    _xpath_estatistica_a_button = (
        "//*[@id=\"__chrome\"]//chrome-app/div/nav/div/div/dl/dd[1]/a[aria-label='Estatística'"
        "and class='Link-sc-7welv8-1 eNExiu styles__StyledNavigationListItem-sc-1c80vy6-11 "
        "dsQriY']")
    _xpath_episodios_a_button = (
        "//*[@id=\"__chrome\"]//chrome-app/div/nav/div/div/dl/dd[1]/a[aria-label='Episódios'"
        "and class='LLink-sc-7welv8-1 eNExiu styles__StyledNavigationListItem-sc-1c80vy6-11 dsQriY']")
    _xpath_interacao_a_button = (
        "//*[@id=\"__chrome\"]//chrome-app/div/nav/div/div/dl/dd[1]/a[aria-label='Interação'"
        "and class='Link-sc-7welv8-1 eNExiu styles__StyledNavigationListItem-sc-1c80vy6-11 dsQriY']")
    _xpath_rentabiliza_a_button = (
        "//*[@id=\"__chrome\"]//chrome-app/div/nav/div/div/dl/dd[1]/a[aria-label='Rentabiliza'"
        "and class='Link-sc-7welv8-1 eNExiu styles__StyledNavigationListItem-sc-1c80vy6-11 dsQriY']")
    _xpath_definicoes_a_button = (
        "//*[@id=\"__chrome\"]//chrome-app/div/nav/div/div/dl/dd[1]/a[aria-label='Definições'"
        "and class='Link-sc-7welv8-1 eNExiu styles__StyledNavigationListItem-sc-1c80vy6-11 "
        "dsQriY']")
    _xpath_mensagens_a_button = (
        "//*[@id=\"__chrome\"]//chrome-app/div/nav/div/div/dl/dd[1]/a[aria-label='Mensagens de Domingo'"
        "and class='Link-sc-7welv8-1 eNExiu styles__StyledNavigationListItem-sc-1c80vy6-11 "
        "dsQriY']")
    _xpath_estudos_a_button = (
        "//*[@id=\"__chrome\"]//chrome-app/div/nav/div/div/dl/dd[1]/a[aria-label='Estudos Bíblicos da IQC'"
        "and class='Link-sc-7welv8-1 eNExiu styles__StyledNavigationListItem-sc-1c80vy6-11 "
        "dsQriY']")

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
        self.driver = None
        self.wait = None

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

    def _create_driver(self):
        driver_service = ""
        options = Options()
        # options.add_argument("--headless")

        if platform == "linux" or platform == "linux2":
            driver_service = Service(r'/snap/bin/geckodriver')  # for linux systems
        elif platform == "win32" or platform == "win64":
            driver_service = Service()  # for Windows systems

        self.driver = webdriver.Edge(service=driver_service,
                                     options=options)  # Update this with the path to your webdriver executable

    def _access_spotify(self):
        if self.driver is None:
            self._create_driver()

        if self.wait is None:
            self.wait = WebDriverWait(self.driver, 10)

        try:
            self.driver.get(self.channel_url)
        except TimeoutError as timeout_error:
            print(f"Timeout error: {timeout_error}")
        except TimeoutException as time_out_exception:
            print(f"{time_out_exception}\nURL: {self.channel_url}\n")
        except NoSuchWindowException as window_exception:
            print(f"{window_exception}URL: {self.channel_url}\n")
        except WebDriverException as webdriver_exception:
            print(f"{webdriver_exception}URL: {self.channel_url}\n")
        else:
            if "404" in self.driver.title:
                self.driver.close()
                return "404"
            else:
                self.wait.until(ec.visibility_of_element_located((By.XPATH, self._xpath_login_h1)))
                self.wait.until(ec.visibility_of_element_located((By.XPATH, self._xpath_onetrust_policy_title)))
                if self.driver.find_element(By.XPATH, self._xpath_onetrust_policy_title).is_displayed():
                    self.driver.find_element(By.XPATH, self._xpath_onetrust_policy_button_permit).click()
                return "200"

    def login_spotify(self, username, password):
        if self._access_spotify() == "200":
            self.wait.until(ec.visibility_of_element_located((By.XPATH, self._xpath_continuar_com_spotify_button)))
            # Click on the button "Continuar com o Spotify"
            self.driver.find_element(By.XPATH, self._xpath_continuar_com_spotify_button).click()
            # Wait until the login form is shown on the screen
            self.wait.until(ec.visibility_of_element_located((By.XPATH, self._xpath_iniciar_sessao_title)))
            # Fill the field with the username, password and click login button
            self.driver.find_element(By.XPATH, self._xpath_username_input).send_keys(username)
            self.driver.find_element(By.XPATH, self._xpath_password_input).send_keys(password)
            self.driver.find_element(By.XPATH, self._xpath_login_button).click()
            # If needs to check human verification
            if (self.driver.find_element(By.XPATH, "//*[@id=\"encore-web-main-content\"]/div/div/div/div/div/div/h1")
                    .is_displayed()):
                self.driver.find_element(By.XPATH, "//*[@id=\"recaptcha-anchor\"]/div[1]").click()
                self.driver.find_element(By.XPATH,
                                         "//*[@id=\"encore-web-main-content\"]/div/div/div/div/div/div/button").click()
            # Check if the screen shows the confirmation of identity
            self.wait.until(ec.visibility_of_element_located((By.XPATH, self._xpath_confirmation_identity_button)))
            if self.driver.find_element(By.XPATH, self._xpath_confirmation_identity_button).is_displayed():
                self.driver.find_element(By.XPATH, self._xpath_confirmation_identity_button).click()
            # Wait until the title of the dashboard is displayed
            self.wait.until(ec.visibility_of_element_located((By.XPATH, self._xpath_dashboard_title)))
            if self.driver.find_element(By.XPATH, self._xpath_dashboard_title).is_displayed():
                return self.driver.find_element(By.XPATH, self._xpath_dashboard_title).text

    # Upload content to spotify
    # Needs to verify the type of content to upload (Estudos bíblicos, mensagens)
    # The last date of content uploaded.
    # In order to upload, needs:
    # Mp3 File name path to upload, dates file of the scheduled contents
    # file names of the structure for the description for Estudo Bíblico
    # and for the mensagens
    def upload_content(self, mp3_filename, date_filename):
        print(self.login_spotify())

    def close_driver(self):
        if self.driver is not None:
            self.driver.quit()
