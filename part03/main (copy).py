import os

import youtube_dl
from pytube import Channel, YouTube


def list_channel_videos(channel_id):
  youtube_channel = Channel(channel_id)
  #  = Channel(f"https://www.youtube.com/{channel_id}/featured")
  videos = youtube_channel.videos

  return [video.watch_url for video in videos]


if __name__ == "__main__":
  #video_url = input("Enter the YouTube video URL: ")
  #links = list_channel_videos(str(video_url))
  #for link in links:
  #  print(link)
  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ids_videos = ydl.extract_info("https://www.youtube.com/watch?v=OzMOcYrakZI")
    print(f"Videos {ids_videos.items}")
  
  channel = Channel("https://www.youtube.com/channel/UCZ84hN7gmZgd2J994l0HD5A")
  yt = YouTube("https://www.youtube.com/watch?v=OzMOcYrakZI")
  channel1 = yt.channel_url
  print(channel.videos_url)
  print(yt.channel_url)
  print(channel1)
  print(channel.video_urls)
  for i, video in enumerate(channel):
    print(i, video)
