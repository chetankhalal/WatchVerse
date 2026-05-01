# MyAnimeList API Example
import requests

url = "https://api.jikan.moe/v4/anime"

response = requests.get(url)
data = response.json()
print(data.pagination)