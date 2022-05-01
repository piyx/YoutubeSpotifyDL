from dataclasses import dataclass
import functools

from ytmusicapi import YTMusic

from ytspdl.services.musicservice import MusicService
from ytspdl.models import Song
from ytspdl.models import ResultType
from ytspdl.utils import extract_playlist_id


@dataclass
class Youtube(MusicService):
    client: YTMusic
    
    def _parse_track(self, track: dict) -> Song:
        return Song(
            title=track["title"],
            album=track["album"]["name"] if track["album"] else None,
            artist=track["artists"][0]["name"],
            imgurl=f'https://i.ytimg.com/vi/{track["videoId"]}/sddefault.jpg'
        )

    def _parse_songs(self, results: dict, limit: int, result_type: ResultType) -> list[Song]:     
        match result_type:
            case ResultType.PLAYLIST:
                results = results["tracks"]
            case ResultType.INDIVIDUAL:
                results = results
            case ResultType.LIKED:
                pass

        return [
            self._parse_track(track) 
            for count, track in enumerate(results, 1)
            if count <= limit
        ]
    
    def _fetch_songs(self, api: callable, result_type: ResultType, limit: int = None) -> list[Song]:
        if limit is None:
            limit = 1000
        
        results = api(limit=limit)
        return self._parse_songs(results=results, limit=limit, result_type=result_type)

    def get_playlist_songs(self, playlist_url: str, limit: int = None) -> list[Song]:
        playlist_id = extract_playlist_id(playlist_url=playlist_url)
        api_source = functools.partial(self.client.get_playlist, playlistId=playlist_id)
        return self._fetch_songs(api=api_source, result_type=ResultType.PLAYLIST, limit=limit)

    def get_liked_songs(self, limit: int = None) -> list[Song]:
        raise NotImplementedError("Requires youtube authentication. Not Implemented yet")

    def get_song(self, song_name: str) -> Song:
        results = self.client.search(query=song_name)
        return self._parse_songs(results=results, limit=1, result_type=ResultType.INDIVIDUAL)