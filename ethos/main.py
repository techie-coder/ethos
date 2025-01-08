from player import MusicPlayer
from utils import get_audio_url
from config import get_music_folder
import time

def test_player():
    """
    Temporary function that tests the functionality of the MusicPlayer class.

    This function performs a sequence of tests to validate the behavior of the
    `MusicPlayer` class, including testing playback of songs from a local library and
    online resources. In addition, it verifies various features like setting volume levels
    and controlling playback via pause, resume, and stop operations.

    The function is divided into two main parts:
    1. Testing the library functionality: It initializes a local music library,
       retrieves the available songs, and tests playback along with volume and playback
       controls.
    2. Testing the online playback functionality: It queries for a specific audio track
       URL, plays it, and validates volume and playback controls.

    """
    player = MusicPlayer()
    
    # Test local library
    print("Setting up library...")
    success = player.set_library(str(get_music_folder()))
    if success:
        songs = player.get_library_songs()
        print(f"Found {len(songs)} songs in library")
        
        if songs:
            print("Testing local playback...")
            player.play(songs[0]) # Play the first song in the folder
            time.sleep(5)  
            
            print("Testing volume controls...")
            player.set_volume(50)
            time.sleep(2)
            player.set_volume(100)
            time.sleep(2)
            
            print("Testing pause/resume...")
            player.pause()
            time.sleep(2)
            player.resume()
            time.sleep(50)
            player.stop()
    
    # Test online playback
    print("\nTesting online playback...")
    query = "Rick Astley Never Gonna Give You Up"
    url = get_audio_url(query)
    if url:
        print(f"Playing {query}...")
        player.play(url)
        time.sleep(10)

        print("Testing volume controls...")
        player.set_volume(50)
        time.sleep(5)
        player.set_volume(100)
        time.sleep(2)

        print("Testing pause/resume...")
        player.pause()
        time.sleep(2)
        player.resume()
        time.sleep(50)
        player.stop()

if __name__ == "__main__":
    test_player()
