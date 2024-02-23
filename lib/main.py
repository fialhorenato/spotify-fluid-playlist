import argparse
import logging
from argparse import Namespace
from lib.src.playlist_creator import PlaylistCreator
from src.models.track import Track

scope = [
    "user-library-read",
    "playlist-read-private",
    "playlist-modify-public",
    "playlist-modify-private",
]

def setup_args_parsing() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_id", type=str, help="Id of the playlist on spotify")
    return parser.parse_args()


def setup_logging():
    logging.basicConfig()
    logging.root.setLevel(logging.INFO)


if __name__ == "__main__":
    args = setup_args_parsing()
    playlist_id = args.playlist_id
    PlaylistCreator().create_fluid_playlist(playlist_id)
