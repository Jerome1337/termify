"""
Termify main module
"""
from curses import endwin, initscr, newwin, noecho, textpad
# pylint: disable=W0611
from readline import insert_text
from pynput import keyboard
from sys import exit
from player import Player


class Termify:
    """
    Class Termify contains all the GUI creation/management methods
    """
    player = Player()
    main_screen = initscr()
    exit_termify = False

    def main(self):
        """
        The main method render the correct screen login/player
        and the keyboard listener
        """
        last_token_information = self.player.get_last_token_used()
        logged = self.player.is_logged(last_token_information)

        noecho()

        self.header(self.main_screen)

        if not logged:
            self.login_screen()
        else:
            self.player.login(last_token_information['access_token'])

        self.footer(self.main_screen)
        self.main_screen.refresh()

        listener = keyboard.Listener(on_press=self.controls)
        listener.start()

        # if not self.exited:
        self.player_screen()

    def login_screen(self):
        """
        This method will render the screen used that will ask the user username/id
        and then login if everything asked is correct
        """
        login_title = "Please login using your Spotify username/id:\n"
        login_screen = newwin(0, 0)
        login_screen.box()
        v_dim, h_dim = login_screen.getmaxyx()

        login_screen.addstr(round(v_dim / 2), round((h_dim - len(login_title)) / 2), login_title)

        username_input = login_screen.subwin(1, 44, round(v_dim / 2 + 1), round((h_dim - 44) / 2))
        username_text_input = textpad.Textbox(username_input)
        username_input.refresh()

        login_screen.addstr(v_dim - 1, h_dim - 20, "[Enter]Submit")
        login_screen.refresh()

        username = username_text_input.edit()

        if str(username) != '':
            oauth_win = newwin(0, 0)
            oauth_win.box()
            oauth_win.addstr(v_dim - 1, h_dim - 20, "[Enter]Submit")
            oauth_win.refresh()

            self.player.get_new_token(username)

        endwin()

    def player_screen(self):
        """
        This method will render the main player screen GUI
        with the current track playing and the associated timeline
        """
        while True:
            player = self.player.current_play()
            current_track = next(player)
            v_dim, h_dim = self.main_screen.getmaxyx()

            self.main_screen.addstr(round(v_dim / 2), 1, ' ' * (h_dim - 2))
            self.main_screen.addstr(
                round(v_dim / 2),
                round((h_dim - len(current_track)) / 2),
                current_track
            )
            self.main_screen.refresh()

            for player_state in player:
                self.main_screen.addstr(
                    round(v_dim / 2) + 1,
                    round((h_dim - (len(player_state))) / 2),
                    player_state
                )
                self.main_screen.refresh()

                if not self.player.is_playing:
                    break

                if self.player.is_track_state_changed:
                    self.player.is_track_state_changed = False
                    break

                if self.exit_termify:
                    endwin()
                    exit(0)

    def controls(self, key):
        """
        This method provide Termify player controls handler
        113 is the virtual keycode of the "q" key
        269025044, 269025046, 269025047 are the virtual keycodes
        of media player (previous, start/stop and next) keys

        :param key: The key pressed by the user, sent by the listener created in the main method
        """
        try:
            pressed_key = key.vk
        except AttributeError:
            pressed_key = None

        if pressed_key == 113:
            self.exit_termify = True
        elif pressed_key == 269025047:
            self.player.next_track()
        elif pressed_key == 269025046:
            self.player.previous_track()
        elif pressed_key == 269025044:
            self.player.start_stop_streaming()

    @staticmethod
    def header(screen):
        """
        Add the same header on every screen you pass

        :param screen: The screen where the header will be added
        """
        screen.box()
        titles = ["Welcome on Termify", "Manage your Spotify streaming directly from your terminal"]
        _, h_dim = screen.getmaxyx()

        for index, title in enumerate(titles):
            screen.addstr(index + 1, round((h_dim - len(title)) / 2), title)

    @staticmethod
    def footer(screen):
        """
        Add same footer on every screen you pass

        :param screen: The screen where the footer will be added
        """
        v_dim, _ = screen.getmaxyx()
        screen.addstr(
            v_dim - 1,
            1,
            "(q) quit"
        )


Termify().main()
