import spotipy
import spotipy.util as util


class Login():
    username = ""

    def __init__(self, username):
        self.username = username

    def make_login(self):
        token = util.prompt_for_user_token(self.username, "user-read-currently-playing")

        if token:
            authenticated_client = spotipy.Spotify(auth=token)

            return authenticated_client
        else:
            print("Can't get token for", self.username)
            print("Please retry")
