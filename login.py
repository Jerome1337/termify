"""
This module provide a Spotify authenticated client after OAuth login
This client is used to perform API calls using helpers methods
"""
import spotipy
from spotipy import util


# pylint: disable=R0903
class Login():
    """
    Login class contains login method using Spotipy lib
    """
    username = ""

    def __init__(self, username):
        self.username = username

    def make_login(self):
        """
        Perform a login through OAuth to receive an authenticated client
        """
        client_id = ""
        client_secret = ""
        redirect_url = ""
        token = util.prompt_for_user_token(
            self.username,
            "user-read-currently-playing user-modify-playback-state",
            client_id,
            client_secret,
            redirect_url
        )

        if token:
            authenticated_client = spotipy.Spotify(auth=token)

            return authenticated_client

        print("Can't get token for", self.username)
        print("Please retry")

        return None
