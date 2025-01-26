class Format:
    @staticmethod
    def seconds_to_min_sec(seconds: int) -> str:
        """
        Convert seconds to a string in the format min:sec.

        Args:
        - seconds (int): The duration in seconds.

        Returns:
        - str: The duration in min:sec format.
        """
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02}"


    def resolve_playlists(playlist_path: str) -> list:
        """
        Function to check if any playlist exists.
        
        Args:
        - playlist_path (str): Path to playlist directory
        
        Returns:
        - list: List of playlist files
        """
        import os
        return os.listdir(playlist_path)

    
    def is_recents(recent_file_path: str) -> bool:
        """
        Function to check if any recent file exists.
        
        Args:
        - recent_file_path (str): Path to recents file
        
        Returns:
        - bool: True if file exists, False otherwise
        """
        import os
        return os.path.exists(recent_file_path)

    
    def resolve_recents(recents_path: str) -> list:
        """
        Function to resolve last 5 played songs.
        
        Args:
        - recents_path (str): Path to recents JSON file
        
        Returns:
        - list: List of recent songs
        """
        import json
        if Format.is_recents(recents_path):
            with open(recents_path) as f:
                return json.loads(f.read())
        return []
    
    
    def fetch_tracks_from_playlist(playlist_path: str) -> list:
        """
        Function to fetch all songs from a playlist.json file.

        Args:
        - playlist_path (str): Path to a playlist

        Returns:
        - list: List of all songs in a particular playlist
        """
        import os
        import json
        if os.path.exists(playlist_path):
            with open(playlist_path) as f:
                return json.loads(f.read())
        return []
    
    @staticmethod
    def extract_item_number(entry: str) -> int:
        """Regex method to extract the item number from tracks list"""
        import re
        match = re.match(r'^(\d+)\.', entry)
        if match:
            return int(match.group(1))
        return None
    
    @staticmethod
    def parse_command(command: str):
        """
        Parses commands like '/play after hours' and '/volume 50' to extract values.
    
        Args:
            command (str): The command string to parse
        
        Returns:
            str or int: The extracted value after the command
                - For /play commands: returns the song name as string
                - For /volume commands: returns the volume level as integer
        """
        parts = command.split(maxsplit=1)
    
        if len(parts) != 2:
            raise ValueError("Invalid command format")
        
        command_type, value = parts
    
        if command_type == '/play' or command_type == '/queue-add' or command_type == '/queue-remove':
            return value
        elif command_type == '/volume':
            try:
                return int(value)
            except ValueError:
                raise ValueError("Volume must be a number")
        else:
            raise ValueError("Unknown command")
        
    
    @staticmethod
    def extract_song_and_artist(text: str) -> tuple[str, str]:
        """
        Extracts the song name and artist name from the text in the format:
        <Song No.>.<Song name> by <Artist Name>
        
        Args:
            text (str): The input text.
            
        Returns:
            tuple[str, str]: A tuple containing the song name and artist name.
        """
        import re
        pattern = r'^\d+\.\s*(.+?)\s+by\s+(.+)$'
        match = re.match(pattern, text)
        if match:
            song_name = match.group(1)
            artist_name = match.group(2)
            return song_name, artist_name
        else:
            raise ValueError("Input text is not in the expected format.")

    @staticmethod
    def clean_hashtag(text: str) -> str:
        """Removes the entry number from the track name"""
        import re
        return re.sub(r'^(\d+\. )', r'', text)
