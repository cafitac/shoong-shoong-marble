# game/states.py
from enum import Enum


class GameState(Enum):
    PLAYER_COUNT = "player_count"
    NAME_INPUT = "name_input"
    PLAYING = "playing"
