class Track:
    def __init__(self, uri, name, key=None, mode=None, bpm=None, valence=None, camelot_key=None):
        self.uri = uri
        self.name = name
        self.key = key
        self.camelot_key = camelot_key
        self.mode = mode
        self.bpm = bpm
        self.valence = valence

    def set_bpm(self, bpm: int):
        self.bpm = bpm

    def set_key(self, key: int):
        self.key = key

    def set_mode(self, mode: int):
        self.mode = mode

    def set_valence(self, valence: float):
        self.valence = valence

    def set_camelot_key(self, camelot_key:str):
        self.camelot_key = camelot_key
