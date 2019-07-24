"""
Internal player module
"""
from time import strftime, gmtime, sleep
from authentication import Authentication


class Player(Authentication):
    """
    This class provide all the track management
    and player information
    """
    is_playing = False
    is_track_state_changed = False

    def current_play(self):
        """
        Generate the current playing tracking information and song timeline into yields
        that will be used inside the GUI
        """
        track_information = self.authenticated_client.current_playback()

        try:
            album = track_information["item"]["album"]
            artists_name = []

            for artist in album["artists"]:
                artists_name.append(artist["name"])

            yield f"{', '.join(artists_name)} - {track_information['item']['name']}"

            track_duration = round((int(track_information["item"]["duration_ms"]) / 1000))
            time_elapsed = round((int(track_information["progress_ms"]) / 1000))
            self.is_playing = track_information['is_playing']

            for current_second in range(time_elapsed, track_duration):
                progress = (50 / float(track_duration)) * current_second
                empty = 50 - progress
                time_elapsed = time_elapsed + 1

                # pylint: disable=C0301
                yield f'{self.format_seconds(time_elapsed)} [{"=" * int(progress)}{"-" * int(empty)}] {self.format_seconds(track_duration)}'

                sleep(1)
        except (AttributeError, TypeError):
            yield 'No track is playing'

    def previous_track(self):
        """
        Change the current track to the previous one
        """
        self.authenticated_client.previous_track()
        self.is_track_state_changed = True

    def next_track(self):
        """
        Change the current track to the next one
        """
        self.authenticated_client.next_track()
        self.is_track_state_changed = True

    def start_stop_streaming(self):
        """
        Start/stop current streaming and update global variable used in the GUI
        """
        if self.is_playing:
            self.authenticated_client.pause_playback()
            self.is_playing = False
        else:
            self.authenticated_client.start_playback()
            self.is_playing = True

        self.is_track_state_changed = True

    @staticmethod
    def format_seconds(seconds):
        """
        Format a given seconds amount into human readable time

        :param seconds: Seconds that need to be formatted
        :return: A formatted string representing this seconds amount
        """
        return strftime("%M:%S", gmtime(seconds))
