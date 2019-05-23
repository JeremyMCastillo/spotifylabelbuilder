import sys
import spotipy
import spotipy.util as util
import configparser
import os

scope = 'user-read-recently-played user-top-read user-library-modify user-library-read playlist-modify-public playlist-read-collaborative user-read-email user-read-birthdate user-read-private user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming user-follow-read user-follow-modify'

username = "Jeremy Maxwell Castillo"

config = configparser.ConfigParser()
config.read('config.ini')

token = util.prompt_for_user_token(username, scope, client_id=config['DEFAULT']['SPOTIFY_CLIENT_ID'], client_secret=config['DEFAULT']['SPOTIFY_CLIENT_SECRET'], redirect_uri='http://localhost')

if token:
    sp = spotipy.Spotify(auth=token)
    tracks = sp.album_tracks(sys.argv[1])
    musicDir = config['DEFAULT']['MUSIC_DIR']
    currentTime = 0.0
    fileContents = ""
    separator = ""
    for track in tracks['items']:
        trackName = track['name']
        trackDuration = float(track['duration_ms']) / 1000.0
        fileContents += separator + "{0:.6f}".format(currentTime) + "\t" + "{0:.6f}".format(currentTime + trackDuration) + "\t" + trackName
        currentTime += trackDuration
        separator = "\n"
    album = sp.album(sys.argv[1])
    print(album)
    year = album['release_date'].split('-')[0]
    if not os.path.exists(musicDir + album['artists'][0]['name'] + "\\" + album['name'] + " (" + str(year) + ")"):
        os.makedirs(musicDir + album['artists'][0]['name'] + "\\" + album['name'] + " (" + str(year) + ")")
    file = open(musicDir + album['artists'][0]['name'] + "\\" + album['name'] + " (" + str(year) + ")\\labels.txt", "w+")
    file.write(fileContents)
    file.close()
else:
    print("Can't get token for", username)

