import requests
from spotipy import Spotify
from spotipy import util
from spotify_client_manager import SpotifyClientManager
import os
import pprint

client_manager = SpotifyClientManager()


class Song:
    def __init__(self, title, artist, album, image):
        self.title = title
        self.artist = artist
        self.album = album
        self.image = image

    def __repr__(self):
        return f'Song({self.title}, {self.artist}, {self.album}, {self.image})'

    def __str__(self):
        return f'Song({self.title})'


class SpotifyTracks:
    def __init__(self):
        self.spotify = Spotify(auth=client_manager.get_token)

    def get_cleaned_tracks_data(self, track_ids=None, results=None):
        '''
        Returns a list of songs given a list of track IDs
        song -> contains useful track data
        '''
        if not track_ids and not results:
            return None

        if track_ids:
            results = self.spotify.tracks(track_ids)
            tracks = results['tracks']
            pprint.pprint(tracks[0])

        if results:
            tracks = results['items']
            pprint.pprint(tracks[0])

        songs = []
        for track in tracks:
            album = track['album']['name']
            artist = track['artists'][0]['name']
            title = track['name']
            image = track['album']['images'][0]['url']
            songs.append(Song(title, artist, album, image))

        return songs

    @staticmethod
    def get_track_ids(items):
        '''
        param: items: list of all playlist/album/saved tracks
        '''
        return [item['id'] for item in items]

    def get_album_tracks(self, album_id):
        '''
        Returns a list of all tracks from the given album
        '''
        results = self.spotify.album_tracks(album_id)
        track_ids = SpotifyTracks.get_track_ids(results['items'])
        album_tracks = self.get_cleaned_tracks_data(track_ids)
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
        pprint.pprint(results)
        playlist_tracks = self.get_cleaned_tracks_data(results=results)
        return playlist_tracks

    def get_user_saved_tracks(self):
        '''
        Returns a list of all tracks liked/saved by the user
        '''
        results = self.spotify.current_user_saved_tracks(limit=2)
        pprint.pprint(results)

        track_ids = SpotifyTracks.get_track_ids(results['items'])
        saved_tracks = self.get_cleaned_tracks_data(track_ids)
        return saved_tracks

    def search_track(self, artist_name, song_name):
        '''
        Returns the first track result from the query results if it exists
        Returned as a list so same download function can be used on it.
        '''
        results = self.spotify.search(
            q=f'artist:{artist_name}%20track:{song_name}',
            type='track'
        )

        # Getting the first search result
        track_id = SpotifyTracks.get_track_ids(results['items'][0])
        first_track = self.get_cleaned_tracks_data(track_id)
        return first_track


sp = SpotifyTracks()
# print(sp.get_playlist_tracks('37i9dQZF1DXcRXFNfZr7Tp'))
# print(sp.get_album_tracks('79dL7FLiJFOO0EoehUHQBv'))
print(sp.get_user_saved_tracks())
