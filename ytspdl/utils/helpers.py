import re

import requests
import aiohttp
import yt_dlp

from ytspdl.models import Song


def extract_playlist_id(playlist_url: str) -> str | None:
    '''Extract playlist id from youtube playlist url'''
    match = re.match('.*list=(.*)', playlist_url)
    return match and match.group(1)


async def fetch_youtube_video_id_async(song_name: str) -> str | None:
    '''Fetch youtube video id for a given song name asynchronously'''

    # Replacing whitespace with '+' symbol, since search query cannot have whitespace
    query = "+".join(song_name.split()).encode("utf-8")
    url = f"https://www.youtube.com/results?search_query={query}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            vid_ids = re.findall(r"watch\?v=(\S{11})", html)
            return vid_ids[0] if vid_ids else None


def fetch_youtube_video_id(song_name: str) -> str | None:
    '''Fetch youtube video id for a given song name'''

    # Replacing whitespace with '+' symbol, since search query cannot have whitespace
    query = "+".join(song_name.split()).encode("utf-8")
    url = f"https://www.youtube.com/results?search_query={query}"
    html = requests.get(url)
    
    # Search for all video ids in the html page
    video_ids = re.findall(r"watch\?v=(\S{11})", html.text)
    return video_ids[0] if video_ids else None


def get_sanitized_song_name(song: Song) -> str:
    '''Remove all invalid characters from song name'''
    INVALID_CHARACTERS = r"[#<%>&\*\{\?\}/\\$+!`'\|\"=@\.\[\]:]*"
    song_name = re.sub(INVALID_CHARACTERS, "", f"{song.artist} {song.title}")
    return song_name


def download_song_from_youtube(video_url: str, song_path: str) -> None:
    '''Download only audio (m4a) from youtube for the given video url'''
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "outtmpl": song_path, 
        "quiet": True, 
        "no_warnings": True, 
        "newline": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])