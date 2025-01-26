from ethos.player import MusicPlayer, TrackInfo
from ethos.utils import get_audio_url, fetch_tracks_list
from ethos.tools import helper

class EndlessPlayback():
    """Class to enable endless playback of audio tracks"""

    def __init__(self, player: MusicPlayer, queue: list[str], current_track: str):
        self.queue = []
        self.player = player
        self.queue = queue
        self.player.status = player.status

    
    def start_endless_playback(self):
        while True:
            if not self.queue:
                break
            self.player.play(self.queue[-1])
            self.queue.pop()



    