import os
from math import ceil
from typing import Optional
from typing import Iterator

import spotipy
from dotenv import load_dotenv

from utils import Song
from utils import SongType


load_dotenv(".env")

TOKEN = spotipy.prompt_for_user_token(
    scope="user-library-read",
    username=os.getenv("SPOTIFY_USER_ID"),
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
)

sp = spotipy.Spotify(auth=TOKEN)


class Spotify:
    @staticmethod
    def parse_track(item: dict, song_type: SongType) -> Song:
        # Spotify API has inconsistent response structure
        # This is why response needs to be parsed differently
        # for different song_type

        if song_type in [SongType.ALBUM]:
            return Song(title=item["name"])

        if song_type in [SongType.PLAYLIST, SongType.SAVED]:
            track = item["track"]

        elif song_type in [SongType.SEARCH]:
            track = item

        return Song(
            title=track["name"],
            album=track["album"]["name"],
            artist=track["artists"][0]["name"],
            imgurl=track["album"]["images"][0]["url"],
        )

    @staticmethod
    def get_playlist_songs(playlist_id: str, limit: int = 100) -> Iterator[Song]:
        offset = 0
        calls_required = ceil(limit / 50)
        calls_made = 0
        while calls_made < calls_required:
            data = sp.playlist_tracks(playlist_id, offset=offset, limit=50)
            calls_made += 1

            if "items" not in data or len(data["items"]) == 0:
                return

            if calls_made == calls_required:
                extra = (limit % 50) or 50
                items = data["items"][:extra]
            else:
                items = data["items"]

            for item in items:
                yield Spotify.parse_track(item, SongType.PLAYLIST)

            offset += 50

    @staticmethod
    def get_album_songs(album_id: str) -> Iterator[Song]:
        data = sp.album(album_id)
        artist = data["artists"][0]["name"]
        imgurl = data["images"][0]["url"]
        album = data["name"]

        for item in data["tracks"]["items"]:
            song = Spotify.parse_track(item, SongType.ALBUM)
            song.artist = artist
            song.imgurl = imgurl
            song.album = album
            yield song

    @staticmethod
    def get_saved_songs(limit: int = 50) -> Iterator[Song]:
        offset = 0
        calls_required = ceil(limit / 50)
        calls_made = 0
        while calls_made < calls_required:
            data = sp.current_user_saved_tracks(offset=offset, limit=50)
            calls_made += 1

            if "items" not in data or len(data["items"]) == 0:
                return

            if calls_made == calls_required:
                extra = (limit % 50) or 50
                items = data["items"][:extra]
            else:
                items = data["items"]

            for item in items:
                yield Spotify.parse_track(item, SongType.SAVED)

            offset += 50

    def search_song(artist_name: str, song_name: str) -> Optional[Song]:
        data = sp.search(
            q=f"artist:{artist_name} track:{song_name}", type="track", limit=1
        )

        tracks = data["tracks"]
        if not tracks["items"]:
            return None
        return Spotify.parse_track(tracks["items"][0], SongType.SEARCH)
