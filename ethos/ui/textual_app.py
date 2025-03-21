from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Input
from textual import work
from ethos.ui.rich_layout import RichLayout
from ethos.player import MusicPlayer, TrackInfo
from ethos.tools import helper
from ethos.utils import Search, UserFiles
from ethos.spotify_importer import SpotifyImporter
import random
from functools import lru_cache
import time


class TextualApp(App):
    """Textual Application Class for ethos UI"""

    CSS_PATH = "./styles.tcss"

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+m", "pause", "Pause"),
        ("ctrl+r", "resume", "Resume"),
        ("ctrl+1", "volume_up"),
        ("ctrl+2", "volume_down")
    ]

    player = MusicPlayer()
    helper = helper.Format()
    importer = SpotifyImporter()
    
    volume = 50
    rows_per_page = 10
    start_idx = 0
    should_play_queue = False
    should_play_playlist = False
    show_playlists = False
    add_playlist = False
    import_playlist = False
    
    tracks_list = []
    recents = []
    queue = []
    spotify_playlists = {}
    queue_options = []
    track_to_play = ""
    search_track = ""
    current_track = ""
    select_from_queue = ""
    track_url = ""
    current_track_duration = ""
    layout_widget = ""
    current_playlist = ""
    dashboard_data = ""
    dashboard_title = ""
    
    def __init__(self):
        super().__init__()
        # Add throttle settings
        self.last_update = 0 
        self.min_update_interval = 0.1  # 100ms minimum between updates

    def compose(self) -> ComposeResult:
        """Composer function for textual app"""

        yield RichLayout(id="rich-layout-widget")
        yield Input(placeholder="Type a command")


    def on_mount(self):
        """Handle functions after mounting the app"""

        self.input = reactive("")
        self.recents = UserFiles.fetch_recents()
        self.layout_widget = self.query_one(RichLayout)
        self.player.set_volume(self.volume)

        try:
            if self.recents:
                self.layout_widget.update_dashboard(self.recents, "Recents :-")
            else:
                self.layout_widget.update_dashboard("You have not played any tracks yet!", "")
            self.set_interval(0.25, self.update_)
        except:
            pass

    @work
    async def on_input_submitted(self, event: Input.Submitted):
        """Handle input submission"""

        self.input = event.value
        
        if event.value:
            if not event.value.startswith("/"):
                """Enables data scrolling"""
                if event.value.lower() == "n":
                    """Scroll down"""
                    self.start_idx += self.rows_per_page
                    self.layout_widget.update_dashboard(self.dashboard_data, self.dashboard_title, self.start_idx)
                    
                if event.value.lower() == "p":
                    """Scroll Up"""
                    self.start_idx -= self.rows_per_page if self.start_idx >= 10 else 0
                    self.layout_widget.update_dashboard(self.dashboard_data, self.dashboard_title, self.start_idx)
            
            
            if event.value.startswith("/play") or event.value.startswith("/pl"):
                """Plays a track from spotify search"""
                try:
                    search_track = self.helper.parse_command(event.value)
                    self.layout_widget.update_log("Searching for tracks")
                    self.tracks_list = await Search.fetch_tracks_list(search_track)
                    if self.tracks_list:
                        self.dashboard_data = self.tracks_list
                        self.dashboard_title = "Search Results"
                        self.start_idx = 0
                        self.layout_widget.update_dashboard(self.tracks_list, self.dashboard_title)
                        self.update_input()
                        self.select_from_queue = False
                except ValueError:
                    self.layout_widget.update_dashboard("Invalid command. Make sure to enter a valid command. You can see the list of commands using /help", "")
                    pass
                    

            if event.value.isdigit() and not self.select_from_queue and not self.add_playlist:
                try:
                    if int(event.value) > 0:
                        self.should_play_queue = False
                        self.track_to_play = self.tracks_list[int(event.value)-1]
                        self.handle_play(self.track_to_play)
                        self.layout_widget.update_log("Playing track from search")
                        self.update_input()
                except:
                    pass
                
            if event.value.startswith("/alb"):
                """Searches and plays an album"""
                try:
                    album_name = self.helper.parse_command(event.value)
                    self.layout_widget.update_dashboard(f"Searching for Album: {album_name}", "Album")
                    album = Search.get_album_id(album_name=album_name)
                    album_tracks = Search.get_album_tracks(album)
                    if album_tracks:
                        self.layout_widget.update_log("Fetched Album!")
                        track = album_tracks[0]
                        self.handle_play(track)
                        self.layout_widget.update_log("Playing from Album Search!")
                        self.queue = []
                        del album_tracks[0]
                        self.queue = album_tracks + self.queue     
                except:
                    pass
                
            if event.value == "/pt":
                """Plays a playlist"""
                try:
                    self.show_playlists()
                    self.layout_widget.update_log("Enter playlist number to be played!")
                    self.should_play_playlist = True
                    self.update_input()
                except:
                    pass
                
            if event.value.isdigit() and self.should_play_playlist:
                if int(event.value) > 0:
                    try:
                        ind = int(event.value) - 1
                        playlists = UserFiles.fetch_playlists()
                        playlist = playlists[ind]
                        tracks = UserFiles.fetch_tracks_from_playlist(playlist)
                        self.handle_play(tracks[0])
                        tracks.pop(0)
                        self.queue = tracks + self.queue
                        self.should_play_playlist = not self.should_play_playlist
                    except:
                        pass
            
            if event.value.startswith("/volume") or event.value.startswith("/vl"):
                """Controls the volume of the music player"""
                try:
                    volume_to_be_set = self.helper.parse_command(event.value)
                    self.player.set_volume(volume_to_be_set)
                    self.volume = volume_to_be_set
                    self.update_input()
                    self.layout_widget.update_volume(volume_to_be_set)
                except:
                    self.layout_widget.update_dashboard("Please enter the volume in digits.", "")
                    pass
            
            if event.value.startswith("/queue-add") or event.value.startswith("/qa"):
                """Adds a track to queue"""
                try:
                    self.search_track = self.helper.parse_command(event.value)
                    self.queue_options = await Search.fetch_tracks_list(self.search_track)
                    if self.queue_options:
                        self.dashboard_data = self.queue_options
                        self.dashboard_title = "Type track no. to be added to queue:-"
                        self.start_idx = 0
                        self.layout_widget.update_dashboard(self.queue_options, "Type track no. to be added to queue :-")
                        self.update_input()
                        self.select_from_queue = True
                except:
                    self.layout_widget.update_dashboard("Please enter a valid track name. You can view the list of commands using /help", "")
                    pass

            if event.value.isdigit() and self.select_from_queue and not self.add_playlist:
                try:
                    if int(event.value) > 0:
                        self.should_play_queue = True
                        self.track_to_be_added_to_queue = self.queue_options[int(event.value)-1]
                        self.queue.append(helper.Format.clean_hashtag(self.track_to_be_added_to_queue))
                        self.update_input()
                        self.search_track=""
                except:
                    pass

            if event.value.startswith("/show-queue") or event.value == "/sq":
                """Shows the current queue"""
                try:
                    tracks = self.queue
                    data = []
                    for idx, track in enumerate(tracks):
                        data.append(f"{idx+1}. {track}")
                    self.dashboard_data = data
                    self.dashboard_title = "Current Queue :-"
                    self.start_idx = 0
                    self.layout_widget.update_dashboard(data, "Current Queue :-")
                    self.update_input()
                except:
                    pass

            if event.value.startswith("/pause") or event.value == "/ps":
                """To prevent ui bugs"""
                if str(self.player.get_state()) == "State.Playing":
                    self.action_pause()
                self.update_input()

            if event.value.startswith("/resume") or event.value == "/r":
                """To prevent ui bugs"""
                if str(self.player.get_state()) == "State.Paused":
                    self.action_resume()
                self.update_input()

            if event.value.startswith("/qp"):
                """Plays a specific track from queue"""
                try:
                    ind = int(helper.Format.parse_command(event.value)) - 1
                    if ind > 0:
                        track = self.queue[ind]
                        del self.queue[ind]
                        self.handle_play(track)
                        self.layout_widget.update_log("Playing track from current queue")
                        self.update_input()
                except ValueError:
                    self.layout_widget.update_dashboard("Please enter the no. of track you want to play", "")
                    pass
            
            if event.value == "/recents":
                try:
                    self.recents = UserFiles.fetch_recents()
                    self.start_idx = 0
                    self.layout_widget.update_dashboard(self.recents, "Recents :", self.start_idx)
                    self.update_input()
                except:
                    pass
            
            if event.value.startswith("/cp"):
                """Creates a new playlist"""
                playlist_name = helper.Format.parse_command(event.value)
                UserFiles.create_playlist(playlist_name)
                self.layout_widget.update_dashboard(f"Playlist {playlist_name} was created", "Success")
                
            if event.value == "/sp" or event.value == "/show-playlists":
                """Shows playlists"""
                self.show_playlists()

            if event.value.startswith("/ap"):
                """Adds a track to a particular playlist mentioned!"""
                try:
                    self.current_playlist, track_name = self.helper.parse_command(event.value)
                    self.tracks_list = await Search.fetch_tracks_list(track_name)
                    data = []
                    for idx, track in enumerate(self.tracks_list):
                        data.append(f"{idx+1}. {track}")
                    self.dashboard_data = data
                    self.dashboard_title = f"Enter track number to be added to {self.current_playlist}"
                    self.start_idx = 0
                    self.layout_widget.update_dashboard(self.tracks_list, f"Enter track number to be added to {self.current_playlist}")
                    self.add_playlist = True
                    self.update_input()
                except:
                    pass
            
            if event.value.isdigit() and self.add_playlist:
                try:
                    if int(event.value) > 0:
                        track_name = self.tracks_list[int(event.value) - 1]
                        UserFiles.add_track_to_playlist(self.current_playlist, track_name)
                        self.update_input()
                        self.add_playlist = not self.add_playlist
                        self.update_input()
                except:
                    pass
            
            if event.value.startswith("/vp"):
                """Shows contents of a particular playlist"""
                try: 
                    playlist_name = self.helper.parse_command(event.value)
                    self.show_tracks_from_playlist(playlist_name)
                    self.update_input()
                except:
                    pass
            
            if event.value == "/recents":
                """Shows last 10 tracks played"""
                try:
                    self.recents = UserFiles.fetch_recents()
                    self.layout_widget.update_dashboard(self.recents, "Recents :")
                    self.update_input()
                except:
                    pass

            if event.value == "/sp" or event.value == "/show-playlists":
                """Displays all playlists created or imported by user"""
                self.show_playlists()

            if event.value.startswith("/ap"):
                """Adds a track to playlist"""
                playlist_name, track_name = self.helper.parse_command(event.value)
                self.add_to_playlist(track_name, playlist_name)


            if event.value.startswith("/sf"):
                """Skips forward in the track"""
                try:
                    interval = int(self.helper.parse_command(event.value))
                    if interval:
                        self.player.skip_forward(interval)
                    else:
                        self.player.skip_forward()
                except:
                    pass
            
            if event.value.startswith("/sb"):
                """Skip backward in the track"""
                try:
                    interval = int(self.helper.parse_command(event.value))
                    if interval:
                        self.player.skip_backward(interval)
                    else:
                        self.player.skip_backward()
                except:
                    pass
                
            if event.value == "/next":
                """Plays next track"""
                try:
                    if self.queue:
                        self.handle_play(self.queue[0])
                        del self.queue[0]
                    else:
                        self.layout_widget.update_log("Next track does not exist!")
                except:
                    pass
                
            if event.value == "/prev":
                """Plays previous track"""
                try:
                    if self.queue:
                        self.queue.insert(0, self.current_track)
                    recents = UserFiles.fetch_recents()
                    if recents:
                        prev = recents[1]
                        self.handle_play(prev)
                        self.update_input()
                except:
                    pass
            
            if event.value == "/clq":
                """Clears the queue"""
                try:
                    self.queue = []
                    self.current_track = ""
                except:
                    pass
            
            
            if event.value == "/ip":
                """Prompts user to log in to their spotify for importing playlist"""
                self.layout_widget.update_dashboard("Redirecting you to browser. Please log in to your spotify account to import the playlist of your choice!", "Redirect")
                self.spotify_playlists = self.importer.fetch_playlists()
                data = []
                if self.spotify_playlists:
                    self.layout_widget.update_log("Playlists fetched!")
                    for idx, playlist in enumerate(self.spotify_playlists):
                        data.append(f"{idx+1}. {playlist['name']}")
                    self.dashboard_data = data
                    self.dashboard_title = "Fetched Playlists"
                    self.start_idx = 0
                    self.layout_widget.update_dashboard(data, "Fetched Playlists")
                    self.import_playlist = True
                self.update_input()
                    
            if event.value.isdigit() and self.import_playlist:
                try:
                    choice = int(event.value)
                    if choice > 0:
                        selected_playlist = self.spotify_playlists[choice-1]
                        self.importer.save_playlist_to_json(selected_playlist['id'], selected_playlist['name'])
                        self.layout_widget.update_dashboard(f"Playlist {selected_playlist['name']} saved successfully!", "Success")
                        self.importer.refresh_playlist(selected_playlist['id'], selected_playlist['name'])
                        self.update_input()
                        self.import_playlist = not self.import_playlist
                        self.update_input()
                except:
                    pass
            
            
            if event.value == "/help":
                try:
                    self.layout_widget.show_commands()
                except:
                    pass
            

    def action_pause(self):
        """Pause the player"""
        self.player.pause()
        self.layout_widget.update_playing_status()
        # Clear cached data
        self._last_time = None
        self._last_progress = None


    def action_resume(self):
        """Resume the player"""
        
        if not self.player.is_playing:
            self.player.resume()
            self.layout_widget.update_playing_status()

    def action_volume_up(self):
        """Increase the volume by 5 levels"""
        current_volume = self.player.get_volume()
        self.player.set_volume(current_volume+5)
        self.layout_widget.update_volume(self.player.get_volume())

    def action_volume_down(self):
        """Decrease the volume by 5 levels"""
        current_volume = self.player.get_volume()
        self.player.set_volume(current_volume-5)
        self.layout_widget.update_volume(self.player.get_volume())

    def handle_play(self, track_name: str):
        """Function to handle the track playback"""
        try:
            self.current_track = track_name
            url = self.get_audio_url(track_name)
            self.track_url = url
            self.player.play(url)
            self.player.set_volume(self.volume)
            UserFiles.add_track_to_recents(helper.Format.clean_hashtag(track_name))
            self.layout_widget.update_track(track_name)
            self.current_track_duration = TrackInfo.get_audio_duration(url)
            self.layout_widget.update_total_track_time(TrackInfo.get_audio_duration(url))
            color_ind = random.randint(0,9)
            self.layout_widget.update_color(color_ind)
        except:
            pass
    
    @lru_cache(maxsize=128)
    def get_audio_url(self, track_name: str) -> str:
        """Cache audio URLs to avoid repeated lookups"""
        return Search.get_audio_url(track_name + " official music video")

    def show_playlists(self) -> None:
        try:
            playlists = UserFiles.fetch_playlists()
            # Prepare data in one go
            data = [f"{idx+1}. {playlist}" for idx, playlist in enumerate(playlists)]
            
            # Single update call with all data
            self.dashboard_data = data
            self.dashboard_title = "Playlists"
            self.start_idx = 0
            self.layout_widget.update_dashboard(data, "Your playlists")
        except:
            pass

    def show_tracks_from_playlist(self, playlist: str) -> None:
        try:
            playlist_tracks = UserFiles.fetch_tracks_from_playlist(playlist)
            
            # Paginate results
            page_size = 20
            start = self.start_idx 
            end = start + page_size
            
            current_page = playlist_tracks[start:end]
            data = [f"{idx+1}. {track}" for idx, track in enumerate(current_page, start=start)]
            
            self.dashboard_data = data
            self.dashboard_title = f"Playlist Contents (Page {start//page_size + 1})"
            self.layout_widget.update_dashboard(data, self.dashboard_title)
        except:
            pass

    def add_to_playlist(self, track, playlist: str) -> None:
        try:
            UserFiles.add_track_to_playlist(track, playlist)
            self.layout_widget.update_log("Track added to playlist")
        except:
            pass
            

    def update_input(self) -> None:
        """Function to reset the data in input widget once user enters his input"""
        input_widget = self.query_one(Input)
        input_widget.placeholder = ""
        input_widget.value = ""
    
    @work
    async def update_(self) -> None:
        """Function to update track progress and check for queue"""
        
        current_time = time.time()
        if current_time - self.last_update < self.min_update_interval:
            return
            
        self.last_update = current_time

        try:
            # Cache progress calculations to avoid recalculating every update
            if self.current_track:
                current_time = TrackInfo.get_current_time(self.player)
                progress = int(TrackInfo.get_progress(self.player)) 
                
                # Only update if values changed
                if (current_time != getattr(self, '_last_time', None) or
                    progress != getattr(self, '_last_progress', None)):
                    self.layout_widget.update_music_progress(current_time, progress)
                    self._last_time = current_time
                    self._last_progress = progress
                    
        except:
            pass

        if str(self.player.get_state()) == "State.Ended":
            if self.queue:
                try:
                    track = self.queue[0]
                    self.queue.pop(0)
                    self.handle_play(track)
                    entries = self.queue
                    data = []
                    for idx, entry in enumerate(entries):
                        data.append(f"{idx+1}. {entry}")
                    self.dashboard_data = data
                    self.dashboard_title = "Current Queue:-"
                    self.start_idx = 0
                    self.layout_widget.update_dashboard(data, "Current Queue :-")
                    self.layout_widget.update_log("Currently playing from queue")
                except:
                    pass
            
        if str(self.player.get_state()) == "State.Playing" and not self.queue:
            try:
                self.layout_widget.update_log("Adding new songs to queue") if self.current_track else self.layout_widget.update_log("Queue deleted, play a new song to add new queue!")
                track_suggestions = Search.get_similar_tracks(self.current_track)
                if track_suggestions:
                    self.layout_widget.update_log("Suggestions fetched!")
                for track in track_suggestions:
                    song, artist = helper.Format.extract_song_and_artist(self.current_track)
                    """Prevents duplicate entries since artist top tracks might have the same song thats playing"""
                    if not song in track:
                        self.queue.append(track) 
                self.layout_widget.update_log("Queue updated") if self.queue else self.layout_widget.update_log("")
            except:
                pass