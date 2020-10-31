import requests
from spotipy import Spotify
from spotipy import util
from spotify_client_manager import SpotifyClientManager
from utils import clean_track_data
import os

client_manager = SpotifyClientManager()


class SpotifyTracks:
    def __init__(self):
        self.spotify = Spotify(auth=client_manager.get_token)

    def album_tracks(self, album_id):
        '''
        Returns a list of all tracks from the given album
        '''
        results = self.spotify.album_tracks(album_id)
        album_tracks = []
        for track_data in results:
            song = clean_track_data(track_data)
            album_tracks.append(song)

        return album_tracks

    def get_playlist_tracks(self, playlist_id):
        '''
        Returns a list of all tracks from the given playlist
        '''
        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.get(
            url=query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f'Bearer {client_manager.get_token}'
            }
        )

        results = response.json()
        playlist_tracks = []
        for track_data in results:
            song = clean_track_data(track_data)
            playlist_tracks.append(song)

        return playlist_tracks

    def get_user_saved_tracks(self):
        '''
        Returns a list of all tracks liked/saved by the user
        '''
        results = self.spotify.current_user_saved_tracks(limit=50)

        saved_tracks = []
        for track_data in results:
            song = clean_track_data(track_data)
            saved_tracks.append(song)

        return saved_tracks

    def search_track(self, artist_name, song_name):
        '''
        Returns the first track result from the query results if it exists
        '''
        results = self.spotify.search(
            q=f'artist:{artist_name}%20track:{song_name}',
            type='track'
        )
