import argparse
import logging
from argparse import Namespace

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

scope = [
    "user-library-read",
    "playlist-read-private",
    "playlist-modify-public",
    "playlist-modify-private",
]


class Track:
    def __init__(self, uri, name):
        self.key = None
        self.mode = None
        self.bpm = None
        self.uri = uri
        self.name = name

    def set_bpm(self, bpm: int):
        self.bpm = bpm

    def set_key(self, key: int):
        self.key = key

    def set_mode(self, mode: int):
        self.mode = mode


def main():
    playlist = spotify_client.playlist(playlist_id=playlist_id)
    playlist_name = playlist['name']

    logging.info(f"Playlist Name: {playlist_name}")

    track_objs_list = []
    current_offset = 0

    while True:
        items = spotify_client.playlist_items(playlist_id=playlist_id, limit=50, offset=current_offset)
        playlist_items_to_tracks = map(lambda x: Track(uri=x['track']['uri'], name=x['track']['name']), items['items'])
        track_objs_list.extend(list(playlist_items_to_tracks))
        if items['next'] is None:
            break
        current_offset = items['offset'] + items['limit']

    analyzed_tracks = analyze_tracks(track_objs_list)
    create_new_playlist(analyzed_tracks, playlist_name)


def analyze_tracks(track_obj_list: list[Track]) -> list[Track]:
    track_uris = list(map(lambda x: x.uri, track_obj_list))
    p_list = list(partition(track_uris, 100))

    for my_list in p_list:
        audio_analysis = spotify_client.audio_features(tracks=my_list)

        for track in track_obj_list:
            for track_analysis in audio_analysis:
                if track_analysis['uri'] == track.uri:
                    track.set_bpm(track_analysis['tempo'])
                    track.set_key(track_analysis['key'])
                    track.set_mode(track_analysis['mode'])

    return track_obj_list


def partition(lst: list, size: int) -> list:
    for i in range(0, len(lst), size):
        yield lst[i: i + size]


def create_new_playlist(my_playlist: list[Track], playlist_name: str):
    playlist_fluid: dict[int, list[Track]] = {}

    for track in my_playlist:
        my_list = playlist_fluid.get(track.key, [])
        my_list.append(track)
        playlist_fluid[track.key] = my_list

    for key, value in playlist_fluid.items():
        value.sort(key=lambda x: x.bpm)

    user_id = spotify_client.current_user()['id']
    playlist_new_name = playlist_name + " (Fluid playlist) "

    new_playlist = spotify_client.user_playlist_create(
        user=user_id,
        name=playlist_new_name,
        public=False,
        collaborative=False
    )

    add_items_to_playlist(new_playlist, playlist_fluid)


def add_items_to_playlist(new_playlist: dict, playlist_fluid: dict[int, list[Track]]):
    new_playlist_id = new_playlist['id']
    track_uris = []
    for i in sorted(playlist_fluid.keys()):
        track_uris.extend(list(map(lambda x: x.uri, playlist_fluid[i])))

    p_list = list(partition(track_uris, 100))

    for my_list in p_list:
        spotify_client.playlist_add_items(playlist_id=new_playlist_id, items=my_list)


def login_user() -> Spotify:
    return Spotify(auth_manager=SpotifyOAuth(scope=scope))


def setup_args_parsing() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_id", type=str, help="Id of the playlist on spotify")
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig()
    logging.root.setLevel(logging.INFO)
    args = setup_args_parsing()
    playlist_id = args.playlist_id
    spotify_client = login_user()
    main()
