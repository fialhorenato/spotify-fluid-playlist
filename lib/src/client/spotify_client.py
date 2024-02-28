from typing import List, Any

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from lib.src.models.track import Track
from lib.src.utils.keys_graph import change_pitch_to_camelot

SCOPE = [
    "user-library-read",
    "playlist-read-private",
    "playlist-modify-public",
    "playlist-modify-private",
]


class SpotifyClient:
    def __init__(self):
        self.client = Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))

    def get_current_user(self):
        return self.client.current_user()["id"]

    def create_new_playlist(self, user_id, playlist_name):
        return self.client.user_playlist_create(
            user=user_id, name=playlist_name, public=False, collaborative=False
        )

    def add_songs_to_playlist(self, playlist_id, items):
        self.client.playlist_add_items(playlist_id=playlist_id, items=items)

    def get_playlist_name(self, playlist_id: int) -> str:
        return self.client.playlist(playlist_id=playlist_id).get("name")

    def get_audio_features(self, tracks_name: List[str]) -> dict:
        audio_analysis = self.client.audio_features(tracks=tracks_name)
        return {
            x.get("uri"): {
                "bpm": x.get("tempo"),
                "key": x.get("key"),
                "mode": x.get("mode"),
                "valence": x.get("valence"),
            }
            for x in audio_analysis
        }

    def create_tracks(self, tracks: dict[str, Any], with_audio: bool):
        audio_feature = self.get_audio_features(tracks.keys()) if with_audio else {}
        for music in audio_feature:
            tracks[music] = {**tracks[music], **audio_feature[music]}
        return [
            Track(
                uri=tracks.get(idx).get("uri"),
                name=tracks.get(idx).get("name"),
                bpm=tracks.get(idx).get("bpm"),
                key=tracks.get(idx).get("key"),
                mode=tracks.get(idx).get("mode"),
                valence=tracks.get(idx).get("valence"),
                camelot_key=change_pitch_to_camelot(tracks.get(idx).get("key"),tracks.get(idx).get("mode"))
            )
            for idx in tracks
        ]

    def get_songs_from_playlist(
        self, playlist_id: int, with_audio: bool = False
    ) -> list[Track]:
        tracks = []
        current_offset = 0
        while True:
            items = self.client.playlist_items(
                playlist_id=playlist_id, limit=50, offset=current_offset
            )

            current_tracks = {
                x.get("track").get("uri"): {
                    "uri": x.get("track").get("uri"),
                    "name": x.get("track").get("name"),
                }
                for x in items["items"]
            }
            tracks += self.create_tracks(current_tracks, with_audio)
            if not items.get("next"):
                break
            current_offset = items["offset"] + items["limit"]
        return tracks
