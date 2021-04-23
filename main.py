from threading import Thread

from PyInquirer import prompt
from pathlib import Path
import sys
import os
import re

from dotenv import load_dotenv
from spotifytracks import SpotifyTracks
from youtubetracks import Youtube
from downloader import download

load_dotenv()

MAXVAL = 10000

def ask_platform():
    options = {
        'type': 'list',
        'name': 'choice',
        'message': 'Download From?',
        'choices': [
            '1.Spotify',
            '2.Youtube',
            '3.Exit'
        ]
    }
    return prompt(options)['choice']

def ask_download_option_youtube():
    options = {
        'type': 'list',
        'name': 'choice',
        'message': 'What do you want to do?',
        'choices': [
            '1.Download a playlist',
            '2.Download a particular song',
            '3.Exit'
        ]
    }
    return prompt(options)['choice']

def ask_download_option_spotify():
    options = {
        'type': 'list',
        'name': 'choice',
        'message': 'What do you want to do?',
        'choices': [
            '1.Download your liked songs',
            '2.Download a playlist',
            '3.Download a particular song',
            '4.Exit'
        ]
    }
    return prompt(options)['choice']


def ask_num_songs_to_download():
    options = {
        'type': 'list',
        'name': 'choice',
        'message': 'Select an option.',
        'choices': [
            '1.Download all',
            '2.Enter a custom value:',
            '3.Exit'
        ]
    }

    ans = prompt(options)['choice']

    if '2' in ans:
        number = {
            'type': 'input',
            'name': 'num_songs',
            'message': 'How many songs you want to download?'
        }

        num_songs = prompt(number)['num_songs']
        return int(num_songs)

    elif '3' in ans:
        sys.exit()
    
    return MAXVAL


def ask_download_playlist_songs():
    options = {
        'type': 'input',
        'name': 'id',
        'message': 'Enter playlist id or url (Enter playlist id for youtube):'
    }

    return prompt(options)['id']


def ask_download_particular_song():
    options = [
        {
            'type': 'input',
            'name': 'artist',
            'message': 'Enter artist name:'
        },
        {
            'type': 'input',
            'name': 'song',
            'message': 'Enter song name:'
        }
    ]

    return prompt(options)


def ask_download_path():
    options = {
        'type': 'list',
        'name': 'choice',
        'message': 'Where do you want to download the song?',
        'choices': [
            '1.Current folder',
            '2.Create a new folder here and download',
            '3.Enter a custom download path',
            '4.Exit'
        ]
    }

    choice = prompt(options)['choice']
    if '1' in choice:
        return os.getcwd()

    elif '2' in choice:
        ques = {
            'type': 'input',
            'name': 'folder',
            'message': 'Enter a folder name:'
        }
        folder = prompt(ques)['folder']
        if not os.path.exists(folder):
            os.mkdir(folder)

        return folder

    elif '3' in choice:
        ques = {
            'type': 'input',
            'name': 'path',
            'message': 'Enter path where songs should be downloaded:'
        }

        return prompt(ques)['path']

    else:
        sys.exit()


def spotifydl():
    spotify_tracks = SpotifyTracks()
    choice = ask_download_option_spotify()

    if '1' in choice:
        num_songs = ask_num_songs_to_download()
        songs = spotify_tracks.get_user_saved_tracks(limit=num_songs)

    elif '2' in choice:
        playlist_id = ask_download_playlist_songs()
        if "https" in playlist_id:
            playlist_id = re.search(r'playlist\/(.*)\?', playlist_id).group(1)
        num_songs = ask_num_songs_to_download()
        songs = spotify_tracks.get_playlist_tracks(playlist_id, limit=num_songs)

        if not songs:
            return print('Invalid playlist ID or playlist is empty.')

    elif '3' in choice:
        data = ask_download_particular_song()
        songs = [spotify_tracks.search_track(data['artist'], data['song'])] # List of 1 song

    else:
        sys.exit()

    path = ask_download_path()

    return songs, path

def youtubedl():
    yt = Youtube()
    choice = ask_download_option_youtube()

    if '1' in choice:
        playlist_id = ask_download_playlist_songs()
        num_songs = ask_num_songs_to_download()
        songs = yt.get_playlist_tracks(playlist_id, limit=num_songs)

    elif '2' in choice:
        data = ask_download_particular_song()
        songs = [yt.get_song(f"{data['artist']} {data['song']}")] # List of 1 song
    
    else:
        sys.exit()

    path = ask_download_path()

    return songs, path

def main():
    platform = ask_platform()
    if '1' in platform:
        songs, path = spotifydl()
    
    elif '2' in platform:
        songs, path = youtubedl()
    
    else:
        sys.exit()

    if not os.path.exists(path):
        print('Invalid path')
        return

    os.chdir(Path(path))
    threads = []

    print("Press ctrl+c to stop.")
    for song in songs:
        thread = Thread(target=download, args=(song,), daemon=True)
        threads.append(thread)
        thread.start()
        # download(song)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
