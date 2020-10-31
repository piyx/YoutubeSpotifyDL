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

Song = namedtuple('Song', field_names=['title', 'artist', 'album', 'image'])
DOWNLOAD_PATH = Path('music')

SPACE = ' '*50


class Song:
    def __init__(self, title, artist, album, image):
        this.title = title
        this.artist = artist
        this.album = album
        this.image = image


def spotify_setup():
    scope = 'user-library-read'
    username = os.getenv('SPOTIFY_USER_ID')
    token = util.prompt_for_user_token(username, scope)
    if token:
        spotify = Spotify(auth=token)
        return spotify


def get_song_info(data):
    try:
        track = data['track']
        album = track['album']['name']
        artist = track['artists'][0]['name']
        title = track['name']
        image = track['album']['images'][0]['url']
        return Song(title, artist, album, image)
    except:
        raise SpotifyInfoNotFoundError


def get_yt_url(song_name):
    # Replacing whitespace with '+' symbol
    song_name = '+'.join(song_name.split())
    search_url = f"https://www.youtube.com/results?search_query={song_name}"
    try:
        html = urlopen(search_url).read().decode()
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
    except:
        raise YoutubeDownloadError


def convert_to_mp3(rename):
    try:
        src = 'song.mp4'
        dest = 'song.mp3'
        final = rename + '.mp3'
        os.system(command=f'ffmpeg -i {src} {dest} -loglevel 0')
        os.remove(src)
        os.rename(dest, final)
        return final
    except:
        raise ConvertToMp3Error


def download_song(song_name):
    if os.path.exists(song_name + '.mp3'):
        print(f'{song_name} already exists')
        return 'exists'
    try:
        song_url = get_yt_url(song_name)
        yt = YouTube(song_url)
        yt.streams.get_audio_only().download(filename='song')
        return 'downloaded'
    except:
        raise YoutubeDownloadError


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
    except:
        raise ID3TagError


def create_folder(foldername):
    if not os.path.exists(DOWNLOAD_PATH):
        os.mkdir(DOWNLOAD_PATH)
    os.chdir(DOWNLOAD_PATH)

    if not os.path.exists(foldername):
        os.mkdir(foldername)
    os.chdir(foldername)


def download_tracks(tracks, foldername):
    failed = []
    print('Press ctrl+c to stop')
    for track in tracks:
        song = get_song_info(track)
        song_name = f'{song.artist}-{song.title}'
        print(f'Downloading {song_name} {SPACE}', end='\r')
        status = download_song(song_name)
        if status == 'exists':
            continue
        elif status == 'downloaded':
            song_path = convert_to_mp3(song_name)
            add_tags(song_path, song)
        else:
            failed.append(track)
    print()


def main():
    spotify = spotify_setup()
    results = spotify.current_user_saved_tracks(limit=50)
    tracks = deque(results['items'])
    download_tracks(tracks, 'liked songs')


if __name__ == '__main__':
    main()
