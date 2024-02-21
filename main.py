import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = ["user-library-read", "playlist-read-private"]

def fetch_all_playlists_from_user(spotify_client):
    playlists = spotify_client.current_user_playlists()

    for playlist in playlists['items']:
        id = playlist['id']
        print(f"---------------------------------------------- Playlist name = {id} ----------------------------------------------")
        tracks = spotify_client.playlist_tracks(playlist_id= id)
        
        for track in tracks['items']:
            track_id = track['track']['id']
            track_name = track['track']['name']
            audio_analysis = spotify_client.audio_analysis(track_id=track_id)
            bpm = audio_analysis['track']['tempo']
            key = audio_analysis['track']['key']
            print(f"NAME = {track_name} AND KEY = {key} AND BPM = {bpm}")
    

def login_user():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp
    

if __name__ == "__main__":
    spotify_client = login_user()
    fetch_all_playlists_from_user(spotify_client)


