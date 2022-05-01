"""
Fetch data from library/api and store it in json files and
inspect the results in json files for the data structure.
"""

import json
import os

import dotenv
import spotipy
import ytmusicapi
from spotipy.oauth2 import SpotifyOAuth

from ytspdl.models import MusicServiceData
from ytspdl.utils import extract_playlist_id


# Load environment variables
dotenv.load_dotenv(".env")


# Sample album and playlist url
spotify_json_data_folder = "spotify-json-data"
sample_spotify_playlist_url = "https://open.spotify.com/playlist/37i9dQZF1E8UXBoz02kGID"
sample_spotify_song_query = "flor hold on"

youtube_json_data_folder = "youtube-json-data"
sample_youtube_playlist_url = "https://youtube.com/playlist?list=PLQwVIlKxHM6qv-o99iX9R85og7IzF9YS_"
sample_youtube_song_query = "flor hold on"


def generate_spotify_data() -> MusicServiceData:
    spotify_oauth = SpotifyOAuth(scope=os.getenv("SPOTIPY_SCOPE"))
    spotify = spotipy.Spotify(oauth_manager=spotify_oauth)

    return MusicServiceData(
        liked_songs=spotify.current_user_saved_tracks(),
        playlist_songs=spotify.playlist(sample_spotify_playlist_url),
        individual_song=spotify.search(sample_spotify_song_query),
    )


def generate_youtube_data() -> MusicServiceData:
    youtube = ytmusicapi.YTMusic()
    playlist_id = extract_playlist_id(sample_youtube_playlist_url)

    return MusicServiceData(
        liked_songs=[],
        playlist_songs=youtube.get_playlist(playlist_id),
        individual_song=youtube.search(sample_youtube_song_query),
    )


def write_to_json(directory: str, data_source: callable) -> None:
    liked_songs, playlist_songs, individual_song = data_source()
    os.makedirs(directory, exist_ok=True)

    with (
        open(f"./{directory}/liked_songs.json", "w") as liked_songs_json,
        open(f"./{directory}/playlist_songs.json", "w") as playlist_songs_json,
        open(f"./{directory}/individual_song.json", "w") as individual_song_json,
    ):
        json.dump(liked_songs, liked_songs_json)
        json.dump(playlist_songs, playlist_songs_json)
        json.dump(individual_song, individual_song_json)


if __name__ == "__main__":
    write_to_json(directory=spotify_json_data_folder, data_source=generate_spotify_data)
    write_to_json(directory=youtube_json_data_folder, data_source=generate_youtube_data)