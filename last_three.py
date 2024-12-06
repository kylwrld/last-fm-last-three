import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY")

def get_last_three_from_lastfm_page(user):
    url = f"https://www.last.fm/user/{user}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('tbody', {'data-playlisting-add-entries': True})
    recent_tracks = table.find_all("tr")
    last_three = recent_tracks[0:3]
    result = []
    for song in last_three:
        artist_name = song.find("td", class_="chartlist-artist").text.strip()
        song_name = song.find("td", class_="chartlist-name").text.strip()
        result.append(f"{artist_name} - {song_name}")

    return ", ".join(result)
