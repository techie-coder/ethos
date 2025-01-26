import pytest
import asyncio
from ..ethos.utils import get_audio_url, fetch_tracks_list
from ..ethos.config import get_music_folder
from ..ethos.player import MusicPlayer
import time
player = MusicPlayer()


def test_set_library():
    assert player.set_library(str(get_music_folder()))

def test_get_library_songs():
    assert player.get_library_songs()

def test_get_online_url():
    query = "System of a Down - Chop suey"
    url = get_audio_url(query)
    assert url

def test_local_player():
    print("Setting up library...")
    success = player.set_library(str(get_music_folder()))
    if success:
        songs = player.get_library_songs()
        print(f"Found {len(songs)} songs in library")

        if songs:
            print("Testing local playback...")
            player.play(songs[0])  # Play the first song in the folder
            time.sleep(1)

            print("Testing volume controls...")
            player.set_volume(50)
            time.sleep(1)
            player.set_volume(100)
            time.sleep(1)

            print("Testing pause/resume...")
            player.pause()
            time.sleep(1)
            player.resume()
            time.sleep(1)
            player.stop()
    assert success


def test_online_player():
    print("\nTesting online playback...")
    track_name = "system of a down"
    tracks_list = asyncio.run(fetch_tracks_list(track_name))
    query = tracks_list[0]
    url = get_audio_url(query)
    if url:
        print(f"Playing {query}...")
        player.play(url)
        time.sleep(60)

        print("Testing volume controls...")
        player.set_volume(50)
        time.sleep(1)
        player.set_volume(100)
        time.sleep(1)

        print("Testing pause/resume...")
        player.pause()
        time.sleep(1)
        player.resume()
        time.sleep(1)
        player.stop()
    assert url


test_online_player()

