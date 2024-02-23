import spotipy
from spotipy.oauth2 import SpotifyOAuth
import argparse
import logging

scope = [
    "user-library-read",
    "playlist-read-private",
    "playlist-modify-public",
    "playlist-modify-private",
]


def fetch_all_playlists_from_user():
    playlist = spotify_client.playlist(playlist_id=playlist_id)
    playlist_name = playlist['name']

    logging.info(f"Playlist Name: {playlist_name}")

    track_objs_list = []
    current_offset = 0
    while True:
        items = spotify_client.playlist_items(playlist_id=playlist_id, limit=50, offset=current_offset)
        track_objs_list.extend(list(map(lambda x: {
            'uri': x['track']['uri'],
            'name': x['track']['name'],
        }, items['items'])))

        if items['next'] is None:
            break

        current_offset = items['offset'] + items['limit']

    analyzed_tracks = analyze_tracks(track_objs_list)
    create_new_playlist(analyzed_tracks, playlist_name)


def analyze_tracks(track_obj_list: list):
    track_uris = list(map(lambda x: x['uri'], track_obj_list))
    p_list = list(partition(track_uris, 100))

    for my_list in p_list:
        audio_analysis = spotify_client.audio_features(tracks=my_list)

        for track in track_obj_list:
            for track_analysis in audio_analysis:
                if track_analysis['uri'] == track['uri']:
                    track['bpm'] = track_analysis['tempo']
                    track['key'] = track_analysis['key']

    return track_obj_list


def partition(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i: i + size]


def create_new_playlist(my_playlist: list, playlist_name: str):
    playlist_fluid = {}

    for track in my_playlist:
        my_list = playlist_fluid.get(track['key'], [])
        my_list.append(track)
        playlist_fluid[track['key']] = my_list

    for key, value in playlist_fluid.items():
        value.sort(key=lambda x: x['bpm'])

    user_id = spotify_client.current_user()['id']
    playlist_new_name = playlist_name + " (Fluid playlist) "

    new_playlist = spotify_client.user_playlist_create(
        user=user_id,
        name=playlist_new_name,
        public=False,
        collaborative=False
    )

    add_items_to_playlist(new_playlist, playlist_fluid)


def add_items_to_playlist(new_playlist, playlist_fluid):
    new_playlist_id = new_playlist['id']
    track_uris = []
    for i in sorted(playlist_fluid.keys()):
        track_uris.extend(list(map(lambda x: x['uri'], playlist_fluid[i])))

    p_list = list(partition(track_uris, 100))

    for my_list in p_list:
        spotify_client.playlist_add_items(playlist_id=new_playlist_id, items=my_list)


def login_user():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


if __name__ == "__main__":
    logging.basicConfig()
    logger = logging.getLogger('test')
    logging.root.setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_id", type=str, help="Id of the playlist on spotify")
    args = parser.parse_args()
    playlist_id = args.playlist_id
    spotify_client = login_user()
    fetch_all_playlists_from_user()
