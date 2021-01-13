from urllib.request import urlopen
from dataclasses import dataclass
from spotipy import Spotify
from typing import Union
from spotipy import util
import os
import re

SCOPE = 'user-library-read'
USER_ID = os.getenv('SPOTIFY_USER_ID')
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')



@dataclass
class Song:
    '''
    Song class to store useful track information
    '''
    vidurl: str
    title: str
    artist: str
    album: str
    imgurl: str


@dataclass
class SpotifyClientManager:
    scope: str = SCOPE
    user_id: str = USER_ID
    client_id: str = CLIENT_ID
    client_secret: str = CLIENT_SECRET
    redirect_uri: str = REDIRECT_URI

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


def get_yt_url(song_name: str) -> Union[str, None]:
    '''Get youtube video url from  song name'''
    song_name = '+'.join(song_name.split()).encode('utf-8') # Replacing whitespace with '+' symbol
    search_url = f"https://www.youtube.com/results?search_query={song_name}"
    html = urlopen(search_url).read().decode()
    video_ids = re.findall(r"watch\?v=(\S{11})", html)
    if video_ids:
        return f"https://www.youtube.com/watch?v={video_ids[0]}"
    
    return None


if __name__ == "__main__":
    song = Song(
        vidurl='https://www.youtube.com/watch?v=vi5wR--nuhA',
        title='hold on',
        artist='flor',
        album="come out. you're hiding(deluxe)",
        imgurl='https://i.scdn.co/image/ab67616d0000b273b7f72643bf8a029abeacc5dd'
    )
    print(repr(song))
    print(str(song))

    print(get_yt_url('kupla valentine'))