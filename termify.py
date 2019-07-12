"""
Command module définition
"""
from cmd import Cmd
from termcolor import colored
from spotipy import SpotifyException
from login import Login

class Termify(Cmd):
    """
    Class Termify contains all the command functions
    """
    prompt = colored('Termify> ', 'green')
    intro = "Welcome on Termify"
    doc_leader = "Manage your Spotify streaming direcly from your terminal\n"

    logged = False
    spotify_client = None

    def default(self, line):
        if line in ("x", "q"):
            self.do_exit()
        elif line == "c":
            self.do_current(line)
        elif line == "n":
            self.do_next(line)
        elif line == "p":
            self.do_previous(line)
        else:
            print("Default: {}".format(line))

    def do_login(self, username):
        """
        :param username: Username of the account that will be used by Termify
        """
        if username == "":
            username = input("Give your Spotify username/id please: ")

            login = Login(username)
            self.spotify_client = login.make_login()
            self.logged = True

        print("You are now logged as:", username)

    # pylint: disable=W0613
    def do_exit(self, line):
        """
        Exit Termify by runing exit method
        """
        print("See you next time on Termify")
        return True

    # pylint: disable=W0613
    def do_playback(self, line):
        """
        Start/stop playback of your used device
        """
        self.spotify_client.start_playback()
        print("Playback")

    @classmethod
    def help_playback(cls):
        """
        Documentation of playback command
        """
        print("Start or stop steaming playback")

    # pylint: disable=W0613
    def do_next(self, line):
        """
        Switch to next track
        """
        message = "Switched to next track"

        try:
            self.spotify_client.next_track()
        except SpotifyException as error:
            message = error.msg

        print(message)

    @classmethod
    def help_next(cls):
        """
        Documentation of switching to next track command
        """
        print("Switch current playing track to the next one")

    # pylint: disable=W0613
    def do_previous(self, line):
        """
        Switch to previous track played
        """
        message = "Switched to previous track"

        try:
            self.spotify_client.previous_track()
        except SpotifyException as error:
            message = error.msg

        print(message)

    @classmethod
    def help_previous(cls):
        """
        Documentation of switching to previous track command
        """
        print("Switch current playing track to the previous one")

    # pylint: disable=W0613
    def do_current(self, line):
        """
        Display current track playing
        :param line:
        :return:
        """
        track_information = self.spotify_client.current_playback()
        album = track_information["item"]["album"]
        artists_name = []

        for artist in album["artists"]:
            artists_name.append(artist["name"])

        print(f"{', '.join(artists_name)} - {album['name']}")

    do_EOF = do_exit

Termify().cmdloop()
