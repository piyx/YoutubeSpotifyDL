from InquirerPy.validator import EmptyInputValidator
from InquirerPy.validator import PathValidator
from InquirerPy.base.control import Choice

from ytspdl.models import ResultType
from ytspdl.models import ServiceType

questions = [
    {
        "name": "music_service",
        "message": "Download From?",
        "type": "list",
        "choices": [
            Choice(name="Spotify", value=ServiceType.SPOTIFY),
            Choice(name="Youtube", value=ServiceType.YOUTUBE),
        ]
    },
    {
        "name": "download_choice",
        "message": "What do you want to do?",
        "type": "list",
        "choices": [
            Choice(name="Download a playlist", value=ResultType.PLAYLIST),
            Choice(name="Download liked songs", value=ResultType.LIKED), 
            Choice(name="Download a particular song", value=ResultType.INDIVIDUAL), 
        ]
    },
    {
        "name": "playlist_url",
        "type": "input",
        "message": "Enter playlist url",
        "validate": EmptyInputValidator("Playlist url cannot be empty"),
        "when": lambda x: x["download_choice"] == ResultType.PLAYLIST
    },
    {
        "name": "song_name",
        "type": "input",
        "message": "Enter song name (Title and Artist):",
        "validate": EmptyInputValidator("Song name cannot be empty"),
        "when": lambda x: x["download_choice"] == ResultType.INDIVIDUAL
    },
    {
        "name": "limit",
        "message": "How many songs do you want to download? (Leave blank to download all):",
        "type": "number",
        "default": None,
        "min_allowed": 1,
        "when": lambda x: x["download_choice"] in [ResultType.PLAYLIST, ResultType.LIKED]
    },
    {
        "name": "download_location",
        "type": "filepath",
        "message": "Enter path where you want songs to be downloaded:",
        "only_directories": True,
        "validate": PathValidator()
    }
]