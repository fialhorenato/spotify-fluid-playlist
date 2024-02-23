from typing import List
from lib.src.client.spotify_client import SpotifyClient
from lib.src.models.track import Track
from lib.src.sorted_engine import sort_tracks_by_bpm
from lib.src.utils.utils import partition


class PlaylistCreator:
    def __init__(self):
        self.client = SpotifyClient()

    def split_playlist_by_key(tracks: List[Track]):
        key_playlist = {}
        for track in tracks:
            if track.key not in key_playlist:
                key_playlist[track.key] = {"minor": [], "major": [], "full": []}
            if track.mode:
                key_playlist[track.key].get("major").append(track)
            else:
                key_playlist[track.key].get("minor").append(track)
            key_playlist[track.key].get("full").append(track)
        return key_playlist

    def create_fluid_playlist(self, playlist_id: int):
        playlist_name = self.client.get_playlist_name(playlist_id)
        tracks = self.client.get_songs_from_playlist(playlist_id, with_audio=True)
        key_tracks_splitted = self.split_playlist_by_key(tracks)
        ordered_tracks_by_key_bpm = sort_tracks_by_bpm(key_tracks_splitted)
        user_id = self.client.current_user()["id"]
        playlist_new_name = f"{playlist_name} (Fluid playlist)"

        new_playlist = self.client.user_playlist_create(
            user=user_id, name=playlist_new_name, public=False, collaborative=False
        )

        self.add_items_to_playlist(new_playlist, ordered_tracks_by_key_bpm)
    
    def add_items_to_playlist(self, playlist_obj: dict, tracks: dict[int, list[Track]]):
        new_playlist_id = playlist_obj["id"]
        track_uris = []
        for i in sorted(tracks.keys()):
            track_uris += [x.uri for x in tracks[i].get("full")]

        for my_list in list(partition(track_uris, 100)):
            self.client.playlist_add_items(playlist_id=new_playlist_id, items=my_list)
