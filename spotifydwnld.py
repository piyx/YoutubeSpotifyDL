from spotifyclient import SpotifyClientManager
from spotifytracks import SpotifyTracks
from urllib.request import urlopen
from spotipy import Spotify
from pytube import YouTube
from pathlib import Path
import argparse
import eyed3
import sys
import re
import os

interrupted = False

spotify_tracks = SpotifyTracks()


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


def download_song_from_yt(song_name):
    try:
        song_url = get_yt_url(song_name)
        yt = YouTube(song_url)
        path = yt.streams.get_audio_only().download()
        return os.path.basename(path)
    except Exception as e:
        return None


def convert_to_mp3(src, dest):
    os.system(command=f'ffmpeg -i "{src}" "{dest}" -loglevel 0')
    os.remove(src)


def add_tags(song_path, song):
    image = urlopen(song.image).read()
    audiofile = eyed3.load(song_path)
    tag = audiofile.tag
    tag.artist = song.artist
    tag.title = song.title
    tag.album = song.album
    tag.images.set(3, image, 'image/jpeg')
    tag.save(version=eyed3.id3.ID3_V2_3)


def spotify_download(songs, limit):
    print("Press ctrl+c to stop.")
    skipped, downloaded, error = 0, 0, 0
    for i, song in enumerate(songs[:limit], 1):
        print(f"\rDownloading song {i} of {limit}.", end="")
        name = f'{song.artist} {song.title}'

        song_path = download_song_from_yt(name)

        if not song_path:
            error += 1
            continue

        src = song_path
        dest = os.path.splitext(src)[0] + '.mp3'

        if os.path.exists(dest):
            skipped += 1
            os.remove(src)
            continue

        convert_to_mp3(src, dest)
        add_tags(dest, song)
        downloaded += 1

    print(f"\nDone! Status: [{skipped=}, {error=}, {downloaded=}]")
