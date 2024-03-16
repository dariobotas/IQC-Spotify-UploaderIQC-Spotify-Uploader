import time
from sys import platform

from selenium import webdriver
from selenium.common.exceptions import (
  NoSuchWindowException,
  TimeoutException,
  WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def list_channel_videos(channel_url):
  options = Options()
  options.add_argument("--headless")

  if platform == "linux" or platform == "linux2":
    driver_service = Service(r'/snap/bin/geckodriver')  # for linux systems
  elif platform == "win32" or platform == "win64":
    driver_service = Service()  # for Windows systems
  
  driver = webdriver.Firefox(service=driver_service, options=options)  # Update this with the path to your webdriver executable
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
      # Scroll down to load more videos (This step may vary based on the channel layout)
      for _ in range(5):  # Scroll down 5 times (adjust as needed)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Add a delay to allow more videos to load

      video_elements = driver.find_element(By.XPATH,'//*[@id="video-title"]')
      video_urls = [video_element.get_attribute('href') 
                    for video_element in video_elements]

      driver.quit()

      return video_urls

channel_url = "https://www.youtube.com/channel/UCZ84hN7gmZgd2J994l0HD5A"
videos = list_channel_videos(channel_url)

for video in videos:
    print(video)