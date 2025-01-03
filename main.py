import youtube_channel
import spotify_channel
import variables


def download_youtube_videos():
    channel_videos = input("Paste the Youtube channel: ")
    cmo_channel = youtube_channel.YoutubeChannel(variables.CMO)

    if not channel_videos:
        print(cmo_channel.channel_name)
        print(cmo_channel.channel_url_videos)
        print(cmo_channel.download_youtube_videos_not_downloaded("cmo57.json", "cmo57.json"))
    else:
        cmo_channel = youtube_channel.YoutubeChannel(channel_videos)
        print(cmo_channel.videos_dict())


def upload_spotify_mp3():
    iqc_channel = spotify_channel.SpotifyChannel(variables.IQC_SPOTIFY)
    print(iqc_channel.login_spotify(variables.USERNAME, variables.PASSWORD))
    # iqc_channel.upload_content("","")


if __name__ == "__main__":
    # download_youtube_videos()
    upload_spotify_mp3()
