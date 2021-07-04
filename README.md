# YoutubeSpotifyDL

Youtube and Spotify downloader

## Example

![](imgs/example.gif)

## Setup

1.Create an app: https://developer.spotify.com/dashboard/applications

![](imgs/setup.png)

2.Copy the Client id and client secret

![](imgs/copy.png)

3.Set redirect uri to http://localhost:8888/callback

![](imgs/redirecturi.png)

### Setting Environment Variables (Windows)

`setx SPOTIFY_USER_ID your_user_id`  
`setx SPOTIFY_CLIENT_ID your_client_id`  
`setx SPOTIFY_CLIENT_SECRET your_client_secret`  
`setx SPOTIFY_REDIRECT_URI 'http://localhost:8888/callback'`

Alternatively, if you want to run this program from the current directory, you could use an environment file `.env` and load the credentials from there.

Edit the `.env` file and set the credentials.

## Dependencies

To install all modules run `pip install -r requirements.txt`

## Usage

`python main.py`

## Sample Output

![](imgs/terminal.png)

## Result

![](imgs/folder.png)
![](imgs/musicplayer.png)

## Docker Setup 
You can build a Docker image of this project from the provided Dockerfile.

***Don't forget the dot at the end of the command.***

```sh
docker build -t youtubespotifydl:latest .
```
Before running the image you need to create a `.env` file with the following contents:

`SPOTIFY_USER_ID=your_user_id`  
`SPOTIFY_CLIENT_ID=your_client_id`  
`SPOTIFY_CLIENT_SECRET=your_client_secret`  
`SPOTIFY_REDIRECT_URI=http://server_ip:8888/callback`

For the `SPOTIFY_REDIRECT_URI` variable you will have to provide the Docker Host IP, Docker Container IP or, if you are trying this on a VPS, the public IP of the VPS.

***For some reason `localhost` will not work inside the container. Also make sure to add the `SPOTIFY_REDIRECT_URI` in the Spotify Developer Dashboard***

After building and setting up the `.env` file, you can run the tool with this command:

```sh
docker run --rm -it --env-file .env -v /host/path/to/store/downloads:/downloads -v /host/path/to/store/app:/app youtubespotifydl:latest
```
The container will go through the start up sequence and after it is done it will drop you in a terminal inside the container.
To start the tool just type the following command inside the terminal:
```sh
python3 main.py
```
The app will generate an URL, which you need to open in your browser. The URL will redircet you to authorize with your Spotify Account and afterwards the browser
will generate another URL in the address bar that you will need to copy and paste in the terminal. 

***You are now able to download your music through a Docker Container***

#### Explanation:
1. **--rm** - this option will delete the container after you exit from it.
2. **-it** - this option will provide a interactive shell inside the container
3. **--env-file .env** - this is the location of the `.env` file.
4. **-v /host/path/to/store/downloads:/downloads** - this is to link a folder on your host to a folder in the container. In this case we are linking the downloads folder so that our downloaded muisc persists after the container is shutdown and removed. On the left of the `:` is the host location and on the right is the location inside the container. Feel free to change the left side.
5. **-v /host/path/to/store/app:/app** - same as the point above but for persisting the application itself. This option might be more useful for debuging the app or manual updates with the latest changes but that's about it.
6. **youtubespotifydl:latest** - the actual image name. ***NOTE: If you changed the -t paramater during the build process you will have to reflect that change here as well***

## How it works

```
* Program Gets the deatils of the songs from spotify api (for spotify songs)
  and youtube music api (for youtube songs)
* It then searches the song on youtube and extracts the youtube song url
* The song is then downloaded as m4a from youtube using pafy module
* Metadata are added to the m4a song (Artist, title, album, album art image)
```
