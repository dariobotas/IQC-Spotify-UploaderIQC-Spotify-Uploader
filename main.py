import time
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


def list_channel_videos(channel_url):
    video_urls = []
    driver_service = ""
    options = Options()
    options.add_argument("--headless")

    if platform == "linux" or platform == "linux2":
        driver_service = Service(r'/snap/bin/geckodriver')  # for linux systems
    elif platform == "win32" or platform == "win64":
        driver_service = Service()  # for Windows systems

    driver = webdriver.Edge(service=driver_service,
                               options=options)  # Update this with the path to your webdriver executable
    try:
        driver.get(channel_url)
    except TimeoutError as timeout_error:
        print(f"Timeout error: {timeout_error}")
    except TimeoutException as time_out_exception:
        print(f"{time_out_exception}\nURL: {channel_url}\n")
    except NoSuchWindowException as window_exception:
        print(f"{window_exception}URL: {channel_url}\n")
    except WebDriverException as webdriver_exception:
        print(f"{webdriver_exception}URL: {channel_url}\n")
    else:
        if "404" in driver.title:
            driver.close()
            return "404"
        else:
            # Click consent if it is displayed
            youtube_consent = driver.find_element(
                By.XPATH,
                "//button[contains(@aria-label,'Rejeitar tudo')]//span[contains(text(),'Rejeitar tudo')]")
            if youtube_consent.is_displayed():
                youtube_consent.click()

            # Scroll down to load more videos (This step may vary based on the channel layout)
            last_height = driver.find_elements(By.XPATH, '//*[@id="video-title-link"]')
            actions = ActionChains(driver)
            while True:
                # Scroll down
                actions.scroll_by_amount(0, 10000).perform()
                time.sleep(2)
                # Check the video content on the page
                new_height = driver.find_elements(By.XPATH, '//*[@id="video-title-link"]')
                # To verify if we load all the content
                if len(new_height) == len(last_height):
                    break  # No new content, stop scrolling
                # We have more content to load, need to scroll to check if there is more
                last_height = new_height

            youtube_video_elements = driver.find_elements(By.XPATH, '//*[@id="video-title-link"]')
            video_urls = [video_element.get_attribute('href')
                                                for video_element in youtube_video_elements]

            driver.quit()

            return video_urls


channel_youtube_url = "https://www.youtube.com/channel/UCZ84hN7gmZgd2J994l0HD5A"
cmo_videos = "https://www.youtube.com/@cmo57/videos"
videos = list_channel_videos(cmo_videos)

print(len(videos))
for i, video in enumerate(videos):
    print(f"{i+1}: {video}")
