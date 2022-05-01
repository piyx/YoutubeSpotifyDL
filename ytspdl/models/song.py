from dataclasses import dataclass


@dataclass
class Song:
    """Song entity

    Attributes:
        title: The name of the song
        artist: The artist of the song
        album: The album of the song
        imgurl: The image/thumbnail url for the song
        vidurl: The youtube video url for the song
    """
    title: str = None
    artist: str = None
    album: str = None
    imgurl: str = None
    vidurl: str = None