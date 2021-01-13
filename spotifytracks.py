from collections.abc import Iterator
from typing import Union
from spotipy import Spotify
from spotipy import util
import requests
import pprint
import os

from utils import SpotifyClientManager
from utils import get_yt_url
from utils import Song


token = SpotifyClientManager().get_token


class SpotifyTracks:
    def __init__(self):
        self.spotify = Spotify(auth=token)

    def get_cleaned_track_data(self, item: dict) -> Union[Song, None]:
        ''' Get required useful information from the results
        Eg: Title, artist, album, imgurl

        Parameters:
            - item: json/dictionary containing track data
        '''
        try:
            track = item['track'] if 'track' in item else item
            album = track['album']['name']
            artist = track['artists'][0]['name']
            title = track['name']
            imgurl = track['album']['images'][0]['url']
            return Song(vidurl=None,
                        title=title, 
                        artist=artist, 
                        album=album, 
                        imgurl=imgurl)
        
        except Exception as e:
            print(e)
            return None

    def get_playlist_tracks(self, playlist_id: str, limit: int = None) -> Iterator[Song]:
        ''' Get a list of tracks of a playlist.

        Parameters:
            - playlist_id: the id of the playlist
        '''
        offset = 0
        if limit is None: 
            limit = 10000
        
        fetched = 0
        while offset < limit:
            query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}&limit=50"
            response = requests.get(
                url=query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f'Bearer {token}'
                }
            )

            results = response.json()
            if not response.ok:
                break
            
            if  "items" not in results or not results["items"]:
                return
            
            for item in results['items']:
                fetched += 1
                yield self.get_cleaned_track_data(item)

                if fetched >= limit:
                    return
            
            offset += 50

    def get_user_saved_tracks(self, limit: int = None) -> Iterator[Song]:
        ''' Get a list of the user saved tracks.

        Parameters:
            - playlist_id: the id of the playlist
            - limit: the number of tracks to return. defualt: gets all liked songs
        '''
        offset = 0
        if limit is None:
            limit = 10000

        fetched = 0
        while offset < limit:
            results = self.spotify.current_user_saved_tracks(offset=offset, limit=50)

            if  "items" not in results or not results["items"]:
                return
            
            for item in results['items']:
                fetched += 1
                yield self.get_cleaned_track_data(item)

                if fetched >= limit:
                    return
            
            offset += 50

    def search_track(self, artist_name: str, song_name: str) -> Song:
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
        
        return self.get_cleaned_track_data(results['tracks']['items'][0])


if __name__ == "__main__":
    sp = SpotifyTracks()

    for track in sp.get_playlist_tracks('3sTrt5wr5PT546ka0fxEtv'):
        pprint.pprint(track)
    
    for track in sp.get_user_saved_tracks(limit=300):
        pprint.pprint(track)
    
    pprint.pprint(sp.search_track('flor', 'hold on'))