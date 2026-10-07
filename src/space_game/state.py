from enum import Enum

class GameState(Enum):
    MAIN_MENU = int(0),
    SETTINGS  = int(1),
    GAMEPLAY  = int(2),
    PAUSED    = int(3),
    EXITING   = int(4),