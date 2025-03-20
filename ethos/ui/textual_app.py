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
    
    volume = reactive(50)
    should_play_queue = reactive(False)
    should_play_playlist = reactive(False)
    show_playlists = reactive(False)
    add_playlist = reactive(False)
    import_playlist = reactive(False)
    
    tracks_list = reactive([])
    recents = reactive([])
    queue = reactive([])
    spotify_playlists = reactive({})
    queue_options = reactive([])
    track_to_play = reactive("")
    search_track = reactive("")
    current_track = reactive("")
    select_from_queue = reactive("")
    track_url = reactive("")
    current_track_duration = reactive("")
    layout_widget = ""
    current_playlist = reactive("")
    


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
            self.set_interval(1, self.update_)
        except:
            pass

    @work
    async def on_input_submitted(self, event: Input.Submitted):
        """Handle input submission"""

        self.input = event.value
        
        
        if event.value:
            if event.value.startswith("/play") or event.value.startswith("/pl"):
                try:
                    search_track = self.helper.parse_command(event.value)
                    self.layout_widget.update_log("Searching for tracks")
                    self.tracks_list = await Search.fetch_tracks_list(search_track)
                    if self.tracks_list:
                        self.layout_widget.update_dashboard(self.tracks_list, "Type track no. to be played :-")
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
                try:
                    self.search_track = self.helper.parse_command(event.value)
                    self.queue_options = await Search.fetch_tracks_list(self.search_track)
                    if self.queue_options:
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
                try:
                    tracks = self.queue
                    data = "\n".join(f"{i+1}. {track}" for i, track in enumerate(tracks))
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
                    self.layout_widget.update_dashboard(self.recents, "Recents :")
                    self.update_input()
                except:
                    pass

            if event.value == "/sp" or event.value == "/show-playlists":
                self.show_playlists()

            if event.value.startswith("/ap"):
                """Adds a track to a particular playlist mentioned!"""
                try:
                    self.current_playlist, track_name = self.helper.parse_command(event.value)
                    self.tracks_list = await Search.fetch_tracks_list(track_name)
                    self.layout_widget.update_dashboard(self.tracks_list, f"Enter track number to be added to {self.current_playlist}")
                    self.add_playlist = True
                    self.update_input()
                except:
                    pass
            
            if event.value.isdigit() and self.add_playlist:
                try:
                    if int(event.value) > 0:
                        track_name = self.tracks_list[event.value - 1]
                        UserFiles.add_track_to_playlist(self.current_playlist, track_name)
                        self.update_input()
                except:
                    pass
            
            if event.value.startswith("/vp"):
                """Shows contents of a particular playlist"""
                playlist_name = self.helper.parse_command(event.value)
                self.show_tracks_from_playlist(playlist_name)
                self.update_input()
            
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
                        self.queue.insert(self.current_track)
                    recents = UserFiles.fetch_recents()
                    prev = recents[0]
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
                data = ""
                if self.spotify_playlists:
                    self.layout_widget.update_log("Playlists fetched!")
                    for idx, playlist in enumerate(self.spotify_playlists):
                        data = data + f"{idx+1}. {playlist['name']}" + "\n"
                    data = data + "Type playlist no. to import"
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
            url = Search.get_audio_url(track_name+" official music video")
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
    
    def show_playlists(self) -> None:
        try:
            playlists = UserFiles.fetch_playlists()
            data = ""
            if playlists:
                for idx, playlist in enumerate(playlists):
                    data = data + f"{idx+1}. {playlist}" + "\n"
            self.layout_widget.update_dashboard(data, "Your playlists")
        except:
            pass

    def show_tracks_from_playlist(self, playlist: str) -> None:
        try:
            playlist = UserFiles.fetch_tracks_from_playlist(playlist)
            data = "\n".join(f"{i+1}. {track}" for i, track in enumerate(playlist))
            self.layout_widget.update_dashboard(data, "Playlist Contents :")
        except:
            pass


    def show_tracks_from_playlist(self, playlist: str) -> None:
        try:
            playlist = UserFiles.fetch_tracks_from_playlist(playlist)
            data = "\n".join(f"{i+1}. {track}" for i, track in enumerate(playlist))
            self.layout_widget.update_dashboard(data, "Playlist Contents :")
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
        
        try:   
            self.layout_widget.update_music_progress(TrackInfo.get_current_time(self.player), int(TrackInfo.get_progress(self.player)))
            
        except:
            pass

        if str(self.player.get_state()) == "State.Ended":
            if self.queue:
                try:
                    track = self.queue[0]
                    self.queue.pop(0)
                    self.handle_play(track)
                    entries = self.queue
                    data = "\n".join(f"{i+1}. {track}" for i, track in enumerate(entries))
                    self.layout_widget.update_dashboard(data, "Current Queue :-")
                    self.layout_widget.update_log("Currently playing from queue")
                except:
                    pass
            
        if str(self.player.get_state()) == "State.Playing" and not self.queue:
            try:
                self.layout_widget.update_log("Adding new songs to queue") if self.current_track else self.layout_widget.update_log("Queue deleted, play a new song to add new queue!")
                if self.current_track:
                    self.layout_widget.update_log(self.current_track)
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