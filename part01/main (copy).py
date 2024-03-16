import os
import youtube_dl

def download_youtube_channel(link):
  try:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ids_videos = ydl.extract_info(link)
      print(f"Videos {ids_videos}")
      #ydl.download([link])
    #print(f"Download successful for {link}")
  except youtube_dl.utils.DownloadError as e:
      print(f"Download error: {e}")
  except Exception as e:
      print(f"An error occurred: {e}")

download_youtube_channel("https://www.youtube.com/@cmo57/videos")