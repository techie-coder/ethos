from dataclasses import dataclass

@dataclass
class UIAssets:
    """Data class to store the UI assets for ethos"""


    BRANDING = """        __  .__                  
  _____/  |_|  |__   ____  ______
_/ __ \   __\  |  \ /  _ \/  ___/
\  ___/|  | |   Y  (  <_> )___ \ 
 \___  >__| |___|  /\____/____  >
     \/          \/           \/ """
    

    CAT_SYMBOL = """                                                            
                                                            
                                                            
                                    :=*=                    
                                  .*#-.#=                   
                          .-+*#%%%%%*+-+#                   
                 .=+***++#@@@@@@@@@@@@@@%.                  
                 %#:.:#@@@@@@@@@@@@@@@@@@%=                 
                 *#.=%@@@@@@@@@@@@+=+#@@@@%+                
                  #%@@@@@%#*#@@@@@%@@@@@@%%%=               
                   %%%@@%++*%@%#%@@@@@@%%%%%=               
                  .@@%%%@@@@@@#-#@@%%%%%%%@*                
                   %@@@%%%@@@%#= .*%%%%%@@*.                
                   =@@@@@%%%@@@#--%@@@@@#-                  
                    =*%@@@@%%@@@@@@@@%%%.                   
                      .:-*@@@@@@@@@@@@@@-                   
              :**+       =@@@@@@%@@@@@@@-                   
             *#.        .%@@@@@@@%%%@@@@:                   
            =%         .#@@@@@@@@@@%%%@#                    
            +%.       .#%@@@@@@@@@@@@%%*                    
            .%#:     .*%@@@@@#@@%#@@@@@%=                   
             .+%#++*%%@@@#@@@##@*%@@@#@@-                   
                .----.-%@+#@@%=@+@@@*%%=                    
                  ....:-*=:***===**+=*=:....                
"""


    BUTTON_SYMBOLS = {
        "playing": "↻      ◁     ||     ▷       ↺",
        "paused": "↻      ◁     ▷     ▷       ↺"
    }

    COMMANDS = {
        "/play <track name> or /pl": "to play a specific track",
        "/pause or /ps" : "to pause player",
        "/resume or /r": "to resume player",
        "/volume <number> or /vl": "to set volume to a certain %",
        "/sf <seconds>": "to skip forward",
        "/sb <seconds>": "to skip backward",
        "/next": "to play next track from queue",
        "/prev": "to play previous track from queue",
        "/queue-add <track name> or /qa": "to add a track to current queue",
        "/show-queue or /sq": "to show current queue",
        "/recents": "to show recents",
        "/qp <track number>": "to play the track at the given position in queue",
        "/ip": "to import playlists from user's spotify account",
        "/pt": "to play a particular playlist",
        "/cp": "Create a new playlist",
        "/ap <Playlist Name> <Track name>": "to add a track to a playlist mentioned"
    }

