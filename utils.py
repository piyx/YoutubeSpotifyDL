from dataclasses import dataclass
from spotipy import Spotify
from spotipy import util
import os

@dataclass
class Song:
    '''
    Song class to store useful track information
    '''
    title: str
    artist: str
    album: str
    imgurl: str


@dataclass
class SpotifyClientManager:
    scope: str = 'user-library-read'
    user_id: str = os.getenv('SPOTIFY_USER_ID')
    client_id: str = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret: str = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri: str = os.getenv('SPOTIFY_REDIRECT_URI')

    @property
    def get_token(self):
        '''
        Return the access token
        '''
        return util.prompt_for_user_token(
            self.user_id,
            scope=self.scope,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri
        )

if __name__ == "__main__":
    song = Song(
        title='hold on',
        artist='flor',
        album="come out. you're hiding(deluxe)",
        imgurl='https://i.scdn.co/image/ab67616d0000b273b7f72643bf8a029abeacc5dd'
    )
    print(repr(song))
    print(str(song))