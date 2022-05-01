import os

from ytspdl.models import Song
from ytspdl.utils import fetch_youtube_video_id
from ytspdl.utils import add_tags_to_song
from ytspdl.utils import get_sanitized_song_name
from ytspdl.utils import download_song_from_youtube


class SongDownloader:
    def __init__(self, song: Song, download_location: str = "./"):
        self.song = song
        self.download_location = download_location
        self.song_name = get_sanitized_song_name(song=song)
        self.song_path = f"{self.download_location}/{self.song_name}.m4a"

        if self.song.vidurl is None:
            video_id = fetch_youtube_video_id(song_name=self.song_name)
            self.song.vidurl = f"https://www.youtube.com/watch?v={video_id}"

    def download(self):
        print(f"Downloading {self.song_name}...")
        if os.path.exists(self.song_path):
            print(f"Skipping {self.song_name}: Song Already Exists!")
            return

        try:
            download_song_from_youtube(video_url=self.song.vidurl, song_path=self.song_path)
            add_tags_to_song(song_path=self.song_path, song=self.song)
        except Exception as e:
            print(f"Error downloading song {self.song_name}, Error Message: {e.with_traceback()}")
            if os.path.exists(self.song_path):
                os.remove(self.song_path)