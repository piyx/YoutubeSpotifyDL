from pytube import YouTube
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from urllib.request import urlopen
from pathlib import Path
import re
import os
from spotipy import util
import eyed3
import pprint
from collections import namedtuple
import sys
from collections import deque
import argparse

Song = namedtuple('Song', field_names=['title', 'artist', 'album', 'image'])

SPACE = ' '*50
DOWNLOAD_PATH = Path('./music')
if not os.path.exists(DOWNLOAD_PATH):
    os.mkdir(DOWNLOAD_PATH)


def setup():
    scope = 'user-library-read'
    username = os.getenv('SPOTIFY_USER_ID')
    token = util.prompt_for_user_token(username, scope)
    if token:
        spotify = Spotify(auth=token)
        return spotify


def get_song_info(song):
    track = song['track']
    album = track['album']['name']
    artist = track['artists'][0]['name']
    title = track['name']
    image = track['album']['images'][0]['url']
    return Song(title, artist, album, image)


def get_yt_url(song_name):
    # Replacing whitespace with '+' symbol
    song_name = '+'.join(song_name.split())
    search_url = f"https://www.youtube.com/results?search_query={song_name}"
    html = urlopen(search_url).read().decode()
    video_ids = re.findall(r"watch\?v=(\S{11})", html)
    if video_ids:
        return f"https://www.youtube.com/watch?v={video_ids[0]}"


def convert_to_mp3(rename):
    src = 'song.mp4'
    dest = 'song.mp3'
    final = rename + '.mp3'
    if 'Rick' in final:
        final = 'test.mp3'
    os.system(command=f'ffmpeg -i {src} {dest} -loglevel 0')
    os.remove(src)
    os.rename(dest, final)
    return final


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
        print(f"Coudn't download the song {song_name}")
        return 'error'


def add_tags(song_path, song):
    image = urlopen(song.image).read()
    audiofile = eyed3.load(song_path)
    tag = audiofile.tag
    tag.artist = song.artist
    tag.title = song.title
    tag.album = song.album
    tag.images.set(3, image, 'image/jpeg')
    tag.save(version=eyed3.id3.ID3_V2_3)


def download_tracks(tracks, foldername):
    os.chdir(DOWNLOAD_PATH)
    if not os.path.exists(foldername):
        os.mkdir(foldername)
    os.chdir(foldername)
    print('Press ctrl+c to stop')
    while tracks:
        track = tracks.popleft()
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
            tracks.append(track)
    print()


def main():
    spotify = setup()
    results = spotify.current_user_saved_tracks(limit=50)
    tracks = deque(results['items'])
    download_tracks(tracks, 'liked songs')


if __name__ == '__main__':
    main()
