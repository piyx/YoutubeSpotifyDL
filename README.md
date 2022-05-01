# YoutubeSpotifyDL

Youtube and Spotify downloader

## Example

https://user-images.githubusercontent.com/82235530/166157330-1ff1f26e-5feb-4b45-b232-b8e0f41a3520.mp4

## Setup

1.Create an app: https://developer.spotify.com/dashboard/applications

![](images/setup.png)

2.Copy the Client id and client secret and paste the values in `.env file`

![](images/copy.png)

3.Set redirect uri to http://localhost:8888/callback

![](images/redirecturi.png)

## Setting Environment Variables

Edit the `.env` file and set the credentials.
Set the `SPOTIPY_CLIENT_ID` AND `SPOTIPY_CLIENT_SECRET` values.


## How to run

1. Clone the project  
`git clone https://github.com/piyx/YoutubeSpotifyDL.git`  
2. Navigate to the project directory. The path should look like  
`../../YoutubeSpotifyDL`
3. Install Dependencies  
`pip install -r requirements.txt`
4. Install the package locally  
`pip install .`
5. Run main.py inside ytspdl folder  
`python ytspdl/main.py`
