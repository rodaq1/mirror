import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="d04982abd40346378143f4928d011426",
    client_secret="cf6c95bdb8bc45c2ae7ff51b531bfcd3",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
))

def play_song(song):
    results = sp.search(q=song, type='track', limit=1)
    items = results['tracks']['items']
    if not items:
        print(f"Song '{song}' not found.")
        return
    track_uri = items[0]['uri']
    sp.start_playback(uris=[track_uri])
    print(f"Playing {items[0]['name']} by {items[0]['artists'][0]['name']}")

def pause():
    sp.pause_playback()
    print("Playback paused.")

def resume():
    sp.start_playback()
    print("Playback resumed.")

def toggle_play_pause():
    playback = sp.current_playback()
    if playback and playback['is_playing']:
        pause()
    else:
        resume()

def stop():
    sp.pause_playback()
    print("Playback stopped.")

def next_track():
    sp.next_track()
    print("Skipped to next track.")

def previous_track():
    sp.previous_track()
    print("Went back to previous track.")

def get_current_song():
    playback = sp.current_playback()
    if playback and playback['item']:
        song = playback['item']['name']
        artist = playback['item']['artists'][0]['name']
        return f"Currently playing: {song} by {artist}"
    else:
        return "No song is currently playing."
