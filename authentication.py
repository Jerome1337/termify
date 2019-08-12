"""
Spotify authentication module
"""
from os import path
from glob import glob
from json import loads
from spotipy import util, Spotify, oauth2


class Authentication:
    """
    Collection of authentication helping methods
    """
    authenticated_client = None

    def get_new_token(self, username):
        """
        Get JWT token through OAuth of a given username

        :param username: User account that will manage stream
        """
        client_id = ""
        client_secret = ""
        redirect_url = ""
        token = util.prompt_for_user_token(
            username,
            "user-read-playback-state user-modify-playback-state",
            client_id,
            client_secret,
            redirect_url
        )

        if token:
            self.login(token)

            return

    def login(self, token):
        """
        Provide authenticated client from a given JWT token

        :param token: The token used to
        """
        self.authenticated_client = Spotify(auth=token)

    @staticmethod
    def is_logged(token_info):
        """
        Check if a user is already logged

        :param token_info: The found cached token object
        :return: Bool
        """
        if token_info is None:
            return False

        return not oauth2.is_token_expired(token_info)

    @staticmethod
    def get_last_token_used():
        """
        Get the last token object from cache

        :return: The last used token information object
        """
        files = sorted(glob('.cache-*'), key=path.getmtime)

        if files:
            return loads(
                open(files[-1]).read()
            )

        return None
