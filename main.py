import youtube_channel
import spotify_channel


CHANNEL_YOUTUBE_URL = "https://www.youtube.com/channel/UCZ84hN7gmZgd2J994l0HD5A"
CMO_VIDEOS = "https://www.youtube.com/@cmo57/videos"
CMO = "https://www.youtube.com/@cmo57"

if __name__ == "__main__":

    channel_videos = input("Paste the Youtube channel: ")
    cmo_channel = youtube_channel.YoutubeChannel(CMO)

    if not channel_videos:
       channel = youtube_channel.YoutubeChannel(CMO)
       print(channel.channel_name)
       print(channel.channel_url_videos)
       print(channel.download_youtube_videos_not_downloaded("cmo57.json", "cmo57.json"))
    else:
       channel = youtube_channel.YoutubeChannel(channel_videos)
       print(channel.videos_dict())
