def sort_tracks_by_bpm(tracks):

    for key, value in tracks.items():
        value.get("minor").sort(key=lambda x: x.bpm)
        value.get("major").sort(key=lambda x: x.bpm)
        value.get("full").sort(key=lambda x: x.bpm)
    
    return tracks