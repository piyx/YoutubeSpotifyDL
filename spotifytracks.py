import requests
from spotipy import Spotify
from spotipy import util
from spotifyclient import SpotifyClientManager
import os
import pprint

client_manager = SpotifyClientManager()


class Song:
    '''
    Song class to store useful track information
    Eg: Song(
        title='hold on',
        artist='flor',
        album="come out. you're hiding (deluxe)",
        image='https://i.scdn.co/image/ab67616d0000b273b7f72643bf8a029abeacc5dd'
    )
    '''

    def __init__(self, title, artist, album, image):
        self.title = title
        self.artist = artist
        self.album = album
        self.image = image

    def __repr__(self):
        return f'Song({self.title}, {self.artist}, {self.album}, {self.image})'

    def __str__(self):
        return f'{self.title} - {self.artist}'


class SpotifyTracks:
    def __init__(self):
        self.spotify = Spotify(auth=client_manager.get_token)

    def get_cleaned_tracks_data(self, results):
        ''' Get useful information from the results

        Parameters:
            - results: json/dictionary containing tracks data
        '''
        songs = []
        for item in results['items']:
            track = item['track'] if 'track' in item else item

            album = track['album']['name']
            artist = track['artists'][0]['name']
            title = track['name']
            image = track['album']['images'][0]['url']
            songs.append(Song(title, artist, album, image))

        return songs

    def get_playlist_tracks(self, playlist_id, limit=None):
        ''' Get a list of tracks of a playlist.

        Parameters:
            - playlist_id: the id of the playlist
        '''
        offset = 0
        playlist_tracks = []
        if limit is None: limit = 10000
        
        while offset < limit:
            query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}&limit=50"
            response = requests.get(
                url=query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f'Bearer {client_manager.get_token}'
                }
            )

            results = response.json()
            if not response.ok:
                break

            partial_tracks = self.get_cleaned_tracks_data(results)
            
            if not partial_tracks:
                break
            
            playlist_tracks += partial_tracks
            offset += 50
        
        return playlist_tracks[:limit]

    def get_user_saved_tracks(self, limit=None):
        ''' Get a list of the user saved tracks.

        Parameters:
            - playlist_id: the id of the playlist
            - limit: the number of tracks to return. defualt: gets all liked songs
        '''
        offset = 0
        saved_tracks = []
        if limit is None: limit = 10000

        while offset < limit:
            results = self.spotify.current_user_saved_tracks(offset=offset, limit=50)
            partial_results = self.get_cleaned_tracks_data(results)

            if not partial_results:
                break

            saved_tracks += partial_results
            offset += 50

        return saved_tracks[:limit]

    def search_track(self, artist_name, song_name):
        ''' Get a particular track info

        Parameters:
            - artist_name: the name of the artist
            - song_name: the name of the song
        '''
        results = self.spotify.search(
            q=f'artist:{artist_name} track:{song_name}',
            type='track',
            limit=1
        )

        return self.get_cleaned_tracks_data(results['tracks'])


if __name__ == "__main__":
    sp = SpotifyTracks()
    pprint.pprint(sp.get_playlist_tracks('37i9dQZF1DXcRXFNfZr7Tp'))
    pprint.pprint(sp.search_track('flor', 'hold on'))
    pprint.pprint(sp.get_user_saved_tracks(limit=300))

    song = Song(
        title='hold on',
        artist='flor',
        album="come out. you're hiding(deluxe)",
        image='https://i.scdn.co/image/ab67616d0000b273b7f72643bf8a029abeacc5dd'
    )
    print(repr(song))
    print(str(song))
