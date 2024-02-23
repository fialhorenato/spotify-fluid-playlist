# Spotify Fluid Playlist Generator

This project born as a need of mine to create a more fluid playlist
based on key + bpm.

It is currently using the Spotify API.


## How to use

You have to login into [Developer Spotify](https://developer.spotify.com/),
create an app for you, get client id, client secret and run this in your terminal


```bash
pip3 install -r requirements.txt && 
export SPOTIPY_REDIRECT_URI=http://localhost:8080 &&
export SPOTIPY_CLIENT_SECRET={YOUR_CLIENT_SECRET} &&
export SPOTIPY_CLIENT_ID={YOUR_CLIENT_ID} &&
python3 main.py your_playlist_id
```

