from mutagen.mp4 import MP4, MP4Cover
import requests

from ytspdl.models.song import Song


def add_tags_to_song(song_path: str, song: Song) -> None:
    TITLE = "\xa9nam"
    ALBUM = "\xa9alb"
    ARTIST = "\xa9ART"
    ART = "covr"
    f = MP4(song_path)
    f[TITLE] = song.title
    if song.album is not None:
        f[ALBUM] = song.album
    f[ARTIST] = song.artist
    image_response = requests.get(song.imgurl)
    f[ART] = [MP4Cover(image_response.content, MP4Cover.FORMAT_JPEG)]
    f.save()