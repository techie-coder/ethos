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
        "/play <track name>": "to play a specific track",
        "/pause": "to pause player",
        "/resume": "to resume player",
        "/volume <number>": "to set volume to a certain %",
        "/queue-add <track name>": "to add a track to current queue",
        "/show-queue": "to show current queue",
        "/recents": "to show recents",
        "/qp <track number>": "to play the track at the given position in queue"
    }

