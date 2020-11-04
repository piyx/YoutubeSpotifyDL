from spotifyclient import SpotifyClientManager
from spotifytracks import SpotifyTracks
from urllib.request import urlopen
from spotipy import Spotify
from pytube import YouTube
from pathlib import Path
from tqdm import tqdm
import argparse
import eyed3
import re
import os

PATH = Path('C:/Users/ctrla/Music')

space = ' '*50
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
    except:
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


def spotify_download(songs):
    print("Press ctrl+c to stop.")
    for song in tqdm(songs):
        name = f'{song.artist} {song.title}'

        # Check if song exists

        song_path = download_song_from_yt(name)

        if not song_path:
            continue

        src = song_path
        dest = os.path.splitext(src)[0] + '.mp3'

        if os.path.exists(dest):
            os.remove(src)
            continue

        convert_to_mp3(src, dest)
        add_tags(dest, song)


def main():
    # songs = spotify_tracks.get_user_saved_tracks(limit=50)
    choice = int(input(
        f"{'-'*50}\n"
        "SPOTIFYDL\n"
        "1.Download liked songs\n"
        "2.Download a playlist\n"
        "3.Download a particular song\n"
        "Enter choice: "))

    if choice == 1:
        limit = int(input("Enter number of songs to download: "))
        songs = spotify_tracks.get_user_saved_tracks(limit=limit)
    elif choice == 2:
        playlist_id = input("Enter playlist id: ")
        songs = spotify_tracks.get_playlist_tracks(playlist_id)
    elif choice == 3:
        artist = input("Enter artist name: ")
        title = input("Enter song name: ")
        songs = spotify_tracks.search_track(artist, title)
    else:
        print("\nInvalid choice!")
        return

    os.chdir(PATH)
    spotify_download(songs)


if __name__ == "__main__":
    main()
