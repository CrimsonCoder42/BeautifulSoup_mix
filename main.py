from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_CLIENT_ID = "*************************"
SPOTIPY_CLIENT_SECRET = "****************************"

date = input("What year would you like to travel to? YYYY-MM-DD:")
URL = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(URL)
billboard_web_page = response.text
soup = BeautifulSoup(billboard_web_page, "html.parser")
list_of_songs = [song.getText().split(",")[0] for song in soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


song_uris = []
year = date.split("-")[0]

for song in list_of_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


print(song_uris)


