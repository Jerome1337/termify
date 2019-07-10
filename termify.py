from cmd import Cmd
from login import Login
from termcolor import colored


class Termify(Cmd):
    prompt = colored('Termify> ', 'green')
    intro = "Welcome on Termify"
    doc_leader = "Manage your Spotify streaming direcly from your terminal\n"

    logged = False
    spotify_client = None

    def postloop(self):
        if self.logged:
            self.do_login()

    def default(self, input):
        if input == "x" or input == "q":
            return self.do_exit()
        elif input == "c":
            return self.do_current(input)
        elif input == "n":
            return self.do_next(input)
        elif input == "p":
            return self.do_previous(input)

        print("Default: {}".format(input))

    def do_login(self, username):
        if username == "":
            username = input("Give your Spotify username/id please: ")

            LOGIN = Login(username)
            self.spotify_client = LOGIN.make_login()
            self.logged = True

        print("You are now logged as:", username)

    @staticmethod
    def do_exit():
        print("See you next time on Termify")
        return True

    def do_playback(self, input):
        self.spotify_client.start_playback()
        print("Playback")

    def help_playback(self):
        print("Start or stop steaming playback")

    def do_next(self, input):
        self.spotify_client.next_track()
        print("Switched to next track")

    def help_next(self):
        print("Switch current playing track to the next one")

    def do_previous(self, input):
        self.spotify_client.previous_track()
        print("Switched to previous track")

    def help_previous(self):
        print("Switch current playing track to the previous one")

    def do_current(self, input):
        track_information = self.spotify_client.current_playback()
        album = track_information["item"]["album"]
        artists_name = []

        for artist in album["artists"]:
            artists_name.append(artist["name"])

        print(f"{', '.join(artists_name)} - {album['name']}")

    do_EOF = do_exit

Termify().cmdloop()
