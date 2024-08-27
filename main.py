import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET= os.getenv("CLIENT_SECRET")

billboard_url = "https://www.billboard.com/charts/hot-100"
token_url = "https://accounts.spotify.com/api/token"

'''빌보드 100 스크래핑'''
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

response = requests.get(f"{billboard_url}/{date}/")
data = response.text

soup = BeautifulSoup(data, "html.parser")
all_charts = soup.select(selector="li ul li h3")
sone_names = [chart.get_text().strip() for chart in all_charts]


'''Spotify 인증'''
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        cache_path="token.txt",
        redirect_uri ="http://example.com",
        scope="playlist-modify-private",
        show_dialog=True,
        ))

user_id = sp.current_user()["id"]
print(user_id)


'''노래 title로 Spotify 찾기'''
year = date.split("-")[0]
song_list=["U Got It Bad", "How You Remind Me", "Always On Time"]
song_uris = []
for song in song_list:
    result = sp.search(q=f'track:{song} year:{year}', type="track")
    pprint(result)
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


'''플레이리스트 생성'''
playlist_name = f"{date} Billboard 100"
create_response = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)


'''플레이리스트에 노래 추가'''
playlist_id = create_response["id"]
add_response = sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=song_uris, position=None)
pprint(add_response)