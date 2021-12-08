import re
import os

# import pafy
from pytube import YouTube as youtube_dl;
import requests
from mutagen.mp4 import MP4, MP4Cover

from utils import Song
from youtube import Youtube


def download_song_from_yt(vid_url: str, song_name: str, song: Song) -> None:
    """Download song in the current directory and rename it"""
    # vid = pafy.new(vid_url)
    # vid.getbestaudio(preftype="m4a").download(f"{song_name}.m4a")
    
    def completed(*args):
        print(f"Downloaded {song_name}");
        addtags(os.path.join(os.getcwd(), song_name+".m4a"), song);
    vid = youtube_dl(vid_url, on_complete_callback=completed);
    ys = vid.streams.filter(only_audio=True, file_extension='mp4').last();
    ys.download(output_path=os.getcwd(), filename=song_name+".m4a");


def addtags(songpath: str, song: Song) -> None:
    TITLE = "\xa9nam"
    ALBUM = "\xa9alb"
    ARTIST = "\xa9ART"
    ART = "covr"
    f = MP4(songpath)
    f[TITLE] = song.title
    f[ALBUM] = song.album
    f[ARTIST] = song.artist
    res = requests.get(song.imgurl)
    f[ART] = [MP4Cover(res.content, MP4Cover.FORMAT_JPEG)]
    f.save()


def download(song: Song) -> None:
    INVALID = r"[#<%>&\*\{\?\}/\\$+!`'\|\"=@\.\[\]:]*"
    song_name = re.sub(
        INVALID, "", f"{song.artist} {song.title}"
    )  # Remove invalid chars
    print(f"Downloading {song_name}")
    try:
        if song.vidurl is None:
            vid_id = Youtube.get_video_id(song_name)
            song.vidurl = f"https://www.youtube.com/watch?v={vid_id}"

        song_path = f"{song_name}.m4a"

        if os.path.exists(song_path):
            print(f"Skipping {song_name} : Already Downloaded")
            return

        download_song_from_yt(song.vidurl, song_name, song)
        # addtags(song_path, song)
    except Exception as e:
        if os.path.exists(song_path):
            os.remove(song_path)

        print(f"Error downloading {song_name}: {e}")
