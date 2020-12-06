from spotifydwnld import download_song_from_yt
from spotifydwnld import add_tags, convert_to_mp3
from spotifydwnld import spotify_download
from PyInquirer import prompt, Separator
from spotifytracks import SpotifyTracks
from spotifydwnld import get_yt_url
from pathlib import Path
import sys
import os


def ask_download_option():
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


def ask_num_songs_to_download(num_songs_present, is_playlist=False):
    if is_playlist:
        message = f'There are {num_songs_present} songs in playlist.\n'
    else:
        message = f'You have {num_songs_present} liked songs.\n'

    options = {
        'type': 'list',
        'name': 'choice',
        'message': message,
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

    return num_songs_present


def ask_download_playlist_songs():
    options = {
        'type': 'input',
        'name': 'id',
        'message': 'Enter playlist id:'
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


def main():
    spotify_tracks = SpotifyTracks()
    choice = ask_download_option()

    if '1' in choice:
        songs = spotify_tracks.get_user_saved_tracks()
        num_songs = ask_num_songs_to_download(len(songs))

    elif '2' in choice:
        playlist_id = ask_download_playlist_songs()
        songs = spotify_tracks.get_playlist_tracks(playlist_id)

        if not songs:
            return print('Invalid playlist ID or playlist is empty.')

        num_songs = ask_num_songs_to_download(len(songs), is_playlist=True)

    elif '3' in choice:
        data = ask_download_particular_song()
        songs = spotify_tracks.search_track(data['artist'], data['song'])
        num_songs = 1

    else:
        sys.exit()

    path = ask_download_path()

    if not os.path.exists(path):
        print('Invalid path')
        return

    os.chdir(Path(path))
    spotify_download(songs, limit=num_songs)


if __name__ == "__main__":
    main()
