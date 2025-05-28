from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, List

from app.player.impl import Player


class SpaceColor(Enum):
    NONE = 0
    LIGHT_GREEN = 1
    GREEN = 2
    LIGHT_BLUE = 3
    BLUE = 4
    PINK = 5
    PURPLE = 6
    ORANGE = 7
    RED = 8


class BoardSpace(ABC):
    def __init__(self, seq: int, color: Optional[SpaceColor] = None):
        self._seq: int = seq
        self._color: SpaceColor = color if color is not None else SpaceColor.NONE
        self._landed_players: List[Player] = []

    @abstractmethod
    def on_land(self, player: Player):
        ...

    def get_seq(self) -> int:
        return self._seq
