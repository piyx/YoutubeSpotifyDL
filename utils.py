from dataclasses import dataclass
import enum


@dataclass
class Song:
    vidurl: str = None
    title: str = None
    artist: str = None
    album: str = None
    imgurl: str = None


class SongType(enum.Enum):
    PLAYLIST = 1
    ALBUM = 2
    SAVED = 3
    SEARCH = 4
