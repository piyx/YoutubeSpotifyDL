from dataclasses import dataclass
import functools

import spotipy

from ytspdl.services.musicservice import MusicService
from ytspdl.models import Song
from ytspdl.models import ResultType


@dataclass
class Spotify(MusicService):
    client: spotipy.Spotify

    def _parse_track(self, track: dict) -> Song:        
        return Song(
            title=track["name"],
            album=track["album"]["name"],
            artist=track["artists"][0]["name"],
            imgurl=track["album"]["images"][0]["url"]
        )

    def _parse_songs(self, results: dict, result_type: ResultType) -> list[Song]:
        # Spotify has inconsitent response structure
        match result_type:
            case ResultType.PLAYLIST | ResultType.LIKED:
                results = [item["track"] for item in results["items"]]
            case ResultType.INDIVIDUAL:
                results = results["tracks"]["items"]

        return [
            self._parse_track(track) 
            for track in results 
            if track is not None
        ]

    def _fetch_songs(self, api: callable, result_type: ResultType, limit: int = None) -> list[Song]:
        if limit is None: 
            limit = 1000
        
        offset = 0
        songs_fetched = 0
        songs = []
        fetched_all = False

        while not fetched_all and songs_fetched < limit:
            songs_to_fetch = min(limit-songs_fetched, 50)
            results = api(offset=offset, limit=songs_to_fetch)
            
            next_songs = self._parse_songs(results=results, result_type=result_type)
            songs.extend(next_songs)
            
            songs_fetched += len(next_songs)
            offset += len(next_songs)

            if not next_songs:
                fetched_all = True
        
        return songs
    
    def get_playlist_songs(self, playlist_url: str, limit: int = None) -> list[Song]:
        api_source = functools.partial(self.client.playlist_items, playlist_id=playlist_url)
        return self._fetch_songs(api=api_source, result_type=ResultType.PLAYLIST, limit=limit)

    def get_liked_songs(self, limit: int = None) -> list[Song]:
        api_source = self.client.current_user_saved_tracks
        return self._fetch_songs(api=api_source, result_type=ResultType.LIKED, limit=limit)

    def get_song(self, song_name: str) -> list[Song]:
        api_source = functools.partial(self.client.search, q=song_name)
        return self._fetch_songs(api=api_source, result_type=ResultType.INDIVIDUAL, limit=1)