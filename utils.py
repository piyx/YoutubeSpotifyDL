class Song:
    def __init__(self, title, artist, album, image):
        self.title = title
        self.artist = artist
        self.album = album
        self.image = image


def clean_track_data(data):
    '''
    Returns only the use infomation from given data
    '''
    track = data['track']
    album = track['album']['name']
    artist = track['artists'][0]['name']
    title = track['name']
    image = track['album']['images'][0]['url']
    return Song(title, artist, album, image)
