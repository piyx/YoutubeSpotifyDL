from threading import Thread
import os

import InquirerPy
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import dotenv

from ytspdl.services import Youtube
from ytspdl.services import Spotify
from ytspdl.questions import questions
from ytspdl.models import ResultType
from ytspdl.models import ServiceType
from ytspdl.utils import SongDownloader


# Load environment variables
dotenv.load_dotenv(".env")


def main():
    user_inputs = InquirerPy.prompt(questions=questions)
    music_service = None
    
    match user_inputs["music_service"]:
        case ServiceType.SPOTIFY:
            client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=os.getenv("SPOTIPY_SCOPE")))
            music_service = Spotify(client=client)
        case ServiceType.YOUTUBE:
            client = YTMusic()
            music_service = Youtube(client=client)
    
    match user_inputs["download_choice"]:
        case ResultType.PLAYLIST:
            playlist_url = user_inputs["playlist_url"]
            limit = int(user_inputs["limit"]) if user_inputs["limit"] else None
            songs = music_service.get_playlist_songs(playlist_url=playlist_url, limit=limit)
        case ResultType.LIKED:
            limit = int(user_inputs["limit"]) if user_inputs["limit"] else None
            songs = music_service.get_liked_songs(limit=limit)
        case ResultType.INDIVIDUAL:
            song_name = user_inputs["song_name"]
            songs = music_service.get_song(song_name=song_name)
    

    threads = []
    download_location = user_inputs["download_location"]

    print("Press ctrl+c to stop.")
    for song in songs:
        song_downloader = SongDownloader(song=song, download_location=download_location)
        thread = Thread(target=song_downloader.download, daemon=True)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


if __name__=="__main__":
    main()