import requests
from bs4 import BeautifulSoup


def list_channel_videos(channel_url):
  response = requests.get(channel_url)
  print(response.status_code)
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())
    video_urls = []
    for link in soup.find_all('a'):
      href = link.get('href')
      print(href)  
      if href.startswith('/watch?v='):
            video_urls.append(f"https://www.youtube.com{href}")

    return video_urls
  else:
    print(f"Failed to fetch channel content. Status Code: {response.status_code}")
    return []


channel_url = "https://www.youtube.com/@Fireship/videos"#"https://www.youtube.com/channel/UCZ84hN7gmZgd2J994l0HD5A/videos"
videos = list_channel_videos(channel_url)
print("Here")
print(videos)
for video in videos:
    print(video)