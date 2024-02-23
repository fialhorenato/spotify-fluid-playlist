import spotipy
from spotipy.oauth2 import SpotifyOAuth
import argparse

scope = [
    "user-library-read",
    "playlist-read-private",
    "playlist-modify-public",
    "playlist-modify-private"
]


def fetch_all_playlists_from_user(sp_client: spotipy.Spotify):
    playlist = sp_client.playlist(playlist_id=playlist_id)
    playlist_name = playlist['name']

    print(f"----------- Playlist name = {playlist_name} -----------")

    tracks = playlist['tracks']
    my_playlist = []

    for track in tracks['items']:
        track_id = track['track']['id']
        audio_analysis = sp_client.audio_analysis(track_id=track_id)
        my_track = {
            'name': track['track']['name'],
            'uri': track['track']['uri'],
            'bpm': audio_analysis['track']['tempo'],
            'key': audio_analysis['track']['key']
        }
        my_playlist.append(my_track)

    create_new_playlist(sp_client, my_playlist, playlist_name)




def create_new_playlist(sp_client: spotipy.Spotify, my_playlist: list, playlist_name: str):
    playlist_fluid = {}

    for track in my_playlist:
        print(track)
        my_list = playlist_fluid.get(track['key'], [])
        my_list.append(track)
        playlist_fluid[track['key']] = my_list

    for key, value in playlist_fluid.items():
        value.sort(key=lambda x: x['bpm'])

    user_id = sp_client.current_user()['id']
    playlist_new_name = playlist_name + " (Fluid playlist) "

    new_playlist = sp_client.user_playlist_create(
        user=user_id,
        name=playlist_new_name,
        public=False,
        collaborative=False
    )

    new_playlist_id = new_playlist['id']

    for i in sorted(playlist_fluid.keys()):
        for track in playlist_fluid.get(i):
            print(f"Adding {track['name']} to playlist {playlist_name}")
            sp_client.playlist_add_items(playlist_id=new_playlist_id, items=[track['uri']])


def login_user():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_id", type=str, help="Id of the playlist on spotify")
    args = parser.parse_args()
    playlist_id = args.playlist_id
    spotify_client = login_user()
    fetch_all_playlists_from_user(spotify_client)