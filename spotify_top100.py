from bs4 import BeautifulSoup as BS
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Enter your Spotify API ID and Secret code
ID = 'ID'
secret = 'Code'
scope = 'playlist-modify-private'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/",
        client_id= ID,
        client_secret=secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()['id']

#Enter the date you want to go to
date = input('When would you like to travel to? Type the date in the format: YYYY-MM-DD').strip()
url=f'https://www.billboard.com/charts/official-uk-songs/{date}'


page = requests.get(url).text

soup = BS(page,'html.parser')


songs_html = soup.findAll('span', class_='chart-list-item__title-text')

songs = [song.getText() for song in songs_html]

song_uris = []
year = date.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)