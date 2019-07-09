import sys
from time import sleep
from login import Login

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Please give your username!")
    print("usage: python player.py [username]")
    sys.exit()

LOGIN = Login(username)
spotify_client = LOGIN.make_login()
latest_track = None

while True:
    track_information = spotify_client.current_user_playing_track()
    album = track_information["item"]["album"]
    artists_name = []

    for artist in album["artists"]:
        artists_name.append(artist["name"])

    current_track = f"{', '.join(artists_name)} - {album['name']}"

    if latest_track is None or latest_track != current_track:
        latest_track = current_track
        sys.stdout.write("\rNow listening to: \033[31m%s\033[0m" % current_track)
        sys.stdout.flush()

    sleep(30)
