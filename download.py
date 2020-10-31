import os
import re
import sys
import eyed3
import pprint

from errors import *
from pathlib import Path
from spotipy import util
from pytube import YouTube
from spotipy import Spotify
from collections import deque
from collections import namedtuple
from urllib.request import urlopen
from spotipy.oauth2 import SpotifyOAuth

DOWNLOAD_PATH = Path('music')
SPACE = ' '*50

INVALID_SYMBOLS = '''#<%>&*{}/\\$+!`'|=:@"'''


class Song:
    def __init__(self, title, artist, album, image):
        self.title = title
        self.artist = artist
        self.album = album
        self.image = image


def spotify_setup():
    scope = 'user-library-read'
    username = os.getenv('SPOTIFY_USER_ID')
    try:
        token = util.prompt_for_user_token(username, scope)
        if token:
            spotify = Spotify(auth=token)
            return spotify
    except Exception as e:
        print(e)


def get_song_info(data):
    track = data['track']
    album = track['album']['name']
    artist = track['artists'][0]['name']
    title = track['name']
    image = track['album']['images'][0]['url']
    return Song(title, artist, album, image)


def get_yt_url(song_name):
    # Replacing whitespace with '+' symbol
    song_name = '+'.join(song_name.split()).encode('utf-8')
    search_url = f"https://www.youtube.com/results?search_query={song_name}"
    try:
        html = urlopen(search_url).read().decode()
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
    except Exception as e:
        print(e)


def convert_to_mp3(rename):
    src = 'song.mp4'
    dest = 'song.mp3'
    final = rename + '.mp3'
    os.system(command=f'ffmpeg -i {src} {dest} -loglevel 0')
    os.remove(src)
    os.rename(dest, final)
    return final


def add_tags(song_path, song):
    try:
        image = urlopen(song.image).read()
        audiofile = eyed3.load(song_path)
        tag = audiofile.tag
        tag.artist = song.artist
        tag.title = song.title
        tag.album = song.album
        tag.images.set(3, image, 'image/jpeg')
        tag.save(version=eyed3.id3.ID3_V2_3)
    except Exception as e:
        print(e)


def download_song(song_name, song):
    if os.path.exists(song_name + '.mp3'):
        return True
    try:
        song_url = get_yt_url(song_name)
        yt = YouTube(song_url)
        yt.streams.get_audio_only().download(filename='song')
        song_path = convert_to_mp3(song_name)
        add_tags(song_path, song)
        return True
    except Exception as e:
        print(e)
        if os.path.exists('song.mp3'):
            os.remove('song.mp3')
        return False


def download_tracks(tracks, foldername):
    if not os.path.exists(foldername):
        os.mkdir(foldername)
    os.chdir(foldername)

    print('Press ctrl+c to stop..')
    while tracks:
        track = tracks.popleft()
        song = get_song_info(track)
        name = f'{song.artist} - {song.title}'
        name = re.sub('''[#<%>&*{}/\\$+!`'|=:@"]''', '', name)
        print(f'Downloading {name}..{SPACE}', end='\r')
        status = download_song(name, song)
        if not status:
            print(f'Error downloading {name}')

    print(f'Download complete. {SPACE}')


def main():
    spotify = spotify_setup()

    if not os.path.exists(DOWNLOAD_PATH):
        os.mkdir(DOWNLOAD_PATH)
    os.chdir(DOWNLOAD_PATH)

    playlist_items = spotify.user_playlist()
    print(playlist_items)

    results = spotify.current_user_saved_tracks(limit=50)
    tracks = deque(results['items'])
    download_tracks(tracks, 'likedsongs')


if __name__ == "__main__":
    main()
