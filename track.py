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