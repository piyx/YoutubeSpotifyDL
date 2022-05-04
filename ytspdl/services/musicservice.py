from abc import abstractmethod
from abc import ABC


from ytspdl.models import Song


class MusicService(ABC):
    @abstractmethod
    def get_playlist_songs(self, playlist_url: str, limit: int = None) -> list[Song]:
        ...
    
    @abstractmethod
    def get_liked_songs(self, limit: int = None) -> list[Song]:
        ...

    @abstractmethod
    def get_song(self, song_name: str) -> Song:
        ...
