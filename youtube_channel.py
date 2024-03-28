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


class YoutubeChannel:
    def __init__(self, channel_url):
        self.channel_url = channel_url
        self.channel_url_videos = f"{self.channel_url}/videos"
        self.channel_name = channel_url.split("/")[-1].split("@")[1]

    def videos_dict(self):
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
            driver.get(self.channel_url_videos)
        except TimeoutError as timeout_error:
            print(f"Timeout error: {timeout_error}")
        except TimeoutException as time_out_exception:
            print(f"{time_out_exception}\nURL: {self.channel_url_videos}\n")
        except NoSuchWindowException as window_exception:
            print(f"{window_exception}URL: {self.channel_url_videos}\n")
        except WebDriverException as webdriver_exception:
            print(f"{webdriver_exception}URL: {self.channel_url_videos}\n")
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
                video_titles = [video_element.get_attribute('title')
                                for video_element in youtube_video_elements]
                videos_dict = {
                    title: url
                    for title, url in zip(video_titles, video_urls)
                }

                driver.quit()

                return videos_dict

    def export_videos_to_file(self):
        file_name = f"youtube_video_list_files/{self. channel_name}.json"
        with open(file_name, mode="w") as extract_videos_list:
            json_data = json.dumps(self.videos_dict(), indent=4)
            extract_videos_list.writelines(json_data)
        return file_name

    @staticmethod
    def download_a_youtube_video(youtube_video_url):
        try:
            yt = YouTube(youtube_video_url)
            video = yt.streams.get_audio_only()
            filename = f"{yt.title}.mp3"
            video.download("youtube_mp3_files/", filename=filename)
            print("Video downloaded successfully in mp3!")
        except Exception as e:
            print("An error occurred: ", str(e))

    def download_all_youtube_videos_from_file_list(self, file_name):
        file_path = f"youtube_video_list_files/{file_name}"
        try:
            with open(file_path, mode="r") as youtube_list:
                data = json.load(youtube_list)
        except FileNotFoundError:
            print("File not found. Creating new one")
            self.export_videos_to_file()
        else:
            for key, value in data.items():
                if isinstance(value, str) and value.startswith("https://www.youtube.com/"):
                    try:
                        self.download_a_youtube_video(value)
                    except Exception as e:
                        print(f"Error downloading video '{value}': {e}")
                else:
                    print(f"Skipping non-video link: {value}")

    # Download videos that were not downloaded
    def download_youtube_videos_not_downloaded(self, file_name, file_downloaded_list):
        file_path = f"youtube_video_list_files/{file_name}"
        file_path_list = f"youtube_video_list_files_downloaded/{file_downloaded_list}"
        # Tries to open the list of videos to download. In case of error, creates a new one
        try:
            with open(file_path, mode="r") as file_list_to_download:
                videos_titles_to_download = json.load(file_list_to_download)
        except FileNotFoundError:
            print("File not found. Creating new one")
            name_file = self.export_videos_to_file()
            self.download_youtube_videos_not_downloaded(name_file, file_downloaded_list)
        else:
            # In case of success when open the file, try to open the list of downloaded files
            # If fails to open the list of downloaded files will download anyway and create a new one
            try:
                with open(file_path_list, mode="r") as file_list_downloaded:
                    videos_downloaded = json.load(file_list_downloaded)
            except FileNotFoundError:
                for key, value in videos_titles_to_download.items():
                    if isinstance(value, str) and value.startswith("https://www.youtube.com/"):
                        try:
                            self.download_a_youtube_video(value)
                            with open(file_path_list, mode="a") as file_list_downloaded:
                                json.dump({key:value}, file_list_downloaded, indent=4)
                                print(f"Video information for '{key}' saved to JSON file.")
                        except Exception as e:
                            print(f"Error downloading video '{value}': {e}")
                    else:
                        print(f"Skipping non-video link: {value}")
            else:
                # In case of videos download list file exist, before download a video, will confirm that we didn't
                # download it before
                for key, value in videos_titles_to_download.items():
                    if isinstance(value, str) and value.startswith("https://www.youtube.com/"):
                        if value not in videos_downloaded:
                            try:
                                self.download_a_youtube_video(value)
                                with open(file_path_list, mode="a") as file_list_downloaded:
                                    json.dump({key:value}, file_list_downloaded, indent=4)
                                    print(f"Video information for '{key}' saved to JSON file.")
                            except Exception as e:
                                print(f"Error downloading video '{value}': {e}")
                    else:
                        print(f"Skipping non-video link: {value}")
