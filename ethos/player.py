import vlc
from pathlib import Path
from typing import Optional, List
from config import get_music_folder

class MusicPlayer:
    """
    A music player class for managing audio playback.

    The MusicPlayer class provides functionalities for managing a library of audio
    files, playing, pausing, resuming, stopping tracks, and adjusting volume.
    It integrates with the VLC media player for handling playback.
    """
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.current_track: Optional[str] = None
        self.is_playing = False
        self.library_path: Optional[Path] = get_music_folder()
        
    def set_library(self, path: str) -> bool:
        """Set and validate the music library path"""
        library = Path(path)
        if library.exists() and library.is_dir():
            self.library_path = library
            return True
        return False
    
    def get_library_songs(self) -> List[str]:
        """Get all audio files from the library"""
        if not self.library_path:
            print("Local music folder is not set.")
            return []
            
        audio_extensions = ('.mp3', '.wav', '.flac', '.m4a')
        songs = []
        
        for file in self.library_path.rglob("*"):
            if file.suffix.lower() in audio_extensions:
                songs.append(str(file))
        return songs

    def play(self, track_path: str) -> bool:
        """
        Load and play a music track from a file path or URL.

        This sets the VLC media instance with the specified track and starts playback.

        Args:
        - track_path (str): The full path or URL to the audio track.

        Returns:
        - bool: True if the track was successfully loaded and playback started,
                False otherwise (e.g., invalid file path or VLC initialization error).
        """
        try:
            media = vlc.Media(track_path)
            self.player.set_media(media)
            self.player.play()
            self.current_track = track_path
            self.is_playing = True
            return True
        except Exception:
            return False

    def pause(self):
        """Pause the current playback"""
        if self.is_playing:
            self.player.pause()
            self.is_playing = False

    def resume(self):
        """Resume the paused playback"""
        if not self.is_playing:
            self.player.play()
            self.is_playing = True

    def stop(self):
        """
        Stop the current track playback.

        This stops the VLC media player, resets the current track metadata, and
        sets the playback state to "not playing."
        """
        self.player.stop()
        self.is_playing = False
        self.current_track = None

    def set_volume(self, volume: int):
        """Set volume (0-100)"""
        self.player.audio_set_volume(max(0, min(100, volume)))

    def get_volume(self) -> int:
        """Get current volume"""
        return self.player.audio_get_volume()
    


class TrackInfo:
    """
    A class for managing audio track metadata.

    Provides functionality to retrieve information about audio tracks,
    """
    @staticmethod
    def get_audio_duration(track_path: str) -> int:
        """
        Get the duration of an audio file in seconds.

        Args:
        - audio_path (str): The full path to the audio file.

        Returns:
        - int: The duration of the audio file in seconds, or -1 if the duration
               could not be determined.
        """
        try:
            media = vlc.Media(track_path)
            media_player = vlc.MediaPlayer()
            media_player.set_media(media)

            media.parse_with_options(1, 0)
            while media.get_duration() < 0:
                continue

            return media.get_duration() // 1000  # Convert milliseconds to seconds
        except Exception as e:
            print(f"Error retrieving duration: {e}")
            return -1