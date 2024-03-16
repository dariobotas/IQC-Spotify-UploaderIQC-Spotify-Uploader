import requests

def list_channel_videos(api_key, channel_id):
  base_url = 'https://www.googleapis.com/youtube/v3/search'
  params = {
      'key': api_key,
      'channelId': channel_id,
      'part': 'snippet',
      'order': 'date',
      'type': 'video',
      'maxResults': 10  # Specify the number of videos to retrieve
  }

  response = requests.get(base_url, params=params)

  if response.status_code == 200:
      videos = response.json()['items']
      video_urls = [f'https://www.youtube.com/watch?v={video["id"]["videoId"]}' for video in videos]
      return video_urls
  else:
      print(f"Failed to fetch channel videos. Status Code: {response.status_code}")
      return []

api_key = ''
channel_id = 'UCZ84hN7gmZgd2J994l0HD5A'
videos = list_channel_videos(api_key, channel_id)

for video in videos:
  print(video)
    