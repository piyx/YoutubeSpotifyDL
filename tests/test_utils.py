from ytspdl.utils import extract_playlist_id
from ytspdl.utils import fetch_youtube_video_id


def test_extract_playlist_id():
    playlist_url1 = "https://youtube.com/playlist?list=PLQwVIlKxHM6qv-o99iX9R85og7IzF9YS_"
    playlist_url2 = "https://youtube.com/playlist?somethingrandom"
    
    assert extract_playlist_id(playlist_url1) == "PLQwVIlKxHM6qv-o99iX9R85og7IzF9YS_"
    assert extract_playlist_id(playlist_url2) is None


def test_fetch_youtube_video_url():
    song_name1 = "flor hold on"
    song_name2 = ""

    assert fetch_youtube_video_id(song_name1) is not None
    assert fetch_youtube_video_id(song_name2) is not None


if __name__=="__main__":
    test_extract_playlist_id()
    test_fetch_youtube_video_url()