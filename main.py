import youtube_channel
import spotify_channel


CHANNEL_YOUTUBE_URL = "https://www.youtube.com/channel/UCZ84hN7gmZgd2J994l0HD5A"
CMO_VIDEOS = "https://www.youtube.com/@cmo57/videos"
CMO = "https://www.youtube.com/@cmo57"
IQC_SPOTIFY = "https://podcasters.spotify.com/pod/dashboard/home"
PASSWORD = "IqcMultim3d1a#\"!"
USERNAME = "iqc.multimedia@gmail.com"
USERNAME_DISPOSITIVO = "31bhcyjjfbba2f6sjn5hy54hhmsy"


def download_youtube_videos():
    channel_videos = input("Paste the Youtube channel: ")
    cmo_channel = youtube_channel.YoutubeChannel(CMO)

    if not channel_videos:
        print(cmo_channel.channel_name)
        print(cmo_channel.channel_url_videos)
        print(cmo_channel.download_youtube_videos_not_downloaded("cmo57.json", "cmo57.json"))
    else:
        cmo_channel = youtube_channel.YoutubeChannel(channel_videos)
        print(cmo_channel.videos_dict())


def upload_spotify_mp3():
    iqc_channel = spotify_channel.SpotifyChannel(IQC_SPOTIFY)
    iqc_channel.login_spotify(USERNAME, PASSWORD)


if __name__ == "__main__":
    # download_youtube_videos()
    upload_spotify_mp3()
