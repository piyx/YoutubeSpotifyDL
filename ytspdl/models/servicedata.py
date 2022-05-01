from typing import NamedTuple


JsonType = list | dict


class MusicServiceData(NamedTuple):
    """Data class for music service
    """
    liked_songs: JsonType
    playlist_songs: JsonType
    individual_song: JsonType