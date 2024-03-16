import os
from pytube import YouTube
def download_video(url, output_path):
   try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path)
        print("Video downloaded successfully!")
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    output_path = input("Enter the output path: ")
    download_video(video_url, output_path)
  