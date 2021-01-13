from mutagen.mp4 import MP4, MP4Cover
from collections.abc import Iterator
from urllib.request import urlopen
from dataclasses import dataclass
from ytmusicapi import YTMusic
from typing import Union
import re

from utils import get_yt_url
from utils import Song

@dataclass
class YTSong:
    vidurl: str
    title: str
    album: str
    artist: str
    imgurl: str

class Youtube:
    def __init__(self):
        self.ytmusic = YTMusic()
        self.thumburl = "https://i.ytimg.com/vi/{vid_id}/sddefault.jpg"
        self.vidurl = "https://www.youtube.com/watch?v={vid_id}"
    
    def _get_cleaned_track_data(self, result: dict) -> Song:
        try:
            vid_id = result['videoId']
            title = result['title']
            album = title
            artist = result['artists'][0]['name'] if 'artists' in result else result['author']
            imgurl = self.thumburl.format(vid_id=vid_id)
            
            return Song(vidurl=self.vidurl.format(vid_id=vid_id), 
                        title=title, 
                        artist=artist, 
                        album=album, 
                        imgurl=imgurl)
        
        except Exception as e:
            return None
        
    
    def get_playlist_tracks(self, playlist_id: str, limit: int = None) -> Union[Iterator[Song], None]:
        '''
        Get a genrator of Songs from the given playlist_id
        Works only for public playlists.
        '''
        if limit is None:
            limit = 10000

        try:
            tracks = self.ytmusic.get_playlist(playlist_id, limit=limit)['tracks']
        except KeyError:
            print('Invalid playlist or playlist is empty.')
            return None
        
        for track in tracks:
            yield self._get_cleaned_track_data(track)
    
    def get_song(self, song_name: str) -> Union[Song, None]:
        '''Get Song from a song name'''
        vidurl = get_yt_url(song_name)
        vid_id = re.search(r"watch\?v=(\S{11})", vidurl).group(1)
        return self._get_cleaned_track_data(self.ytmusic.get_song(vid_id))


if __name__ == "__main__":
    yt = Youtube()
    
    for song in yt.get_playlist_tracks('PLxCVu9rqBbd4ebch9FRm3yme-tTl03aa5', 1000):
        print(song)

    print(yt.get_song('flor hold on'))