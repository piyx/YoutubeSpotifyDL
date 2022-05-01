# RESPONSE STRUCTURE

## SPOTIFY

### PLAYLIST RESPONSE

```json
{
    "items": [
        {
            "track": {
                "album": {
                    "name": "album_name"
                    "images": [
                        {"url": "song_thumbnail_url"}
                    ],
                },
                "artists": [
                    {"name": "artist_name"}
                ],
                "name": "song_name"
            }
        }
    ]
}
```

### LIKED SONGS RESPONSE

```json
{
    "items": [
        {
            "track": {
                "album": {
                    "name": "album_name"
                    "images": [
                        {"url": "song_thumbnail_url"}
                    ],
                },
                "artists": [
                    {"name": "artist_name"}
                ],
                "name": "song_name"
            }
        }
    ]
}
```

### INDIVIDUAL SONG RESPONSE

```json
{
    "tracks": {
        "items": [
            {
                "album": {
                    "name": "album_name"
                    "images": [
                        {"url": "song_thumbnail_url"}
                    ],
                },
                "artists": [
                    {"name": "artist_name"}
                ],
                "name": "song_name"
            }
        ]
    }
}
```


## YOUTUBE

### PLAYLIST SONG RESPONSE
```json
{
    "tracks": [
        {
            "title": "song_name",
            "album": {
                "name": "album_name"
            },
            "artists": [
                {
                    "name": "artist_name"
                }
            ],
            "thumbnails": [
                {
                    "url": "song_thumbnail_url"
                }
            ]
        }
    ]
}
```

### INDIVIDUAL SONG RESPONSE
```json
[
    {
        "videoId": "youtube_song_video_id",
        "title": "song_name",
        "album": {
            "name": "album_name"
        },
        "artists": [
            {
                "name": "artist_name"
            }
        ],
        "thumbnails": [
            {
                "url": "song_thumbnail_url"
            }
        ]
    }
]
```