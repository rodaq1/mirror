import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="d04982abd40346378143f4928d011426",
    client_secret="cf6c95bdb8bc45c2ae7ff51b531bfcd3",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
))

def playSong(song):
    results = sp.search(q=song, type='track', limit=1)
    track_uri = results['tracks']['items'][0]['uri']
    sp.start_playback(uris=[track_uri])

sp.pause_playback()

sp.start_playback()

current = sp.current_playback()
print(current['item']['name'])