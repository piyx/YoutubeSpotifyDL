from spotifyclient import SpotifyClientManager
from spotifytracks import SpotifyTracks
from urllib.request import urlopen
from spotipy import Spotify
from pytube import YouTube
from pathlib import Path
from tqdm import tqdm
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
        song_path = download_song_from_yt(name)
        if not song_path:
            continue

        src = song_path
        dest = os.path.splitext(src)[0] + '.mp3'

        convert_to_mp3(src, dest)
        add_tags(dest, song)


def main():
    # songs = spotify_tracks.get_user_saved_tracks(limit=50)
    songs = spotify_tracks.search_track('shawn', 'senorita')
    print(songs)
    os.chdir(PATH)
    spotify_download(songs)


if __name__ == "__main__":
    main()
