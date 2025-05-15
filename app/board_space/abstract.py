from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

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
    _seq: int
    _color: SpaceColor = SpaceColor.NONE
    _landed_players: list[Player] = []

    def __init__(self, seq: int, color: Optional[SpaceColor] = None):
        self._seq = seq
        if color is not None:
            self._color = color

    @abstractmethod
    def on_land(self, player: Player):
        ...

    def get_seq(self) -> int:
        return self._seq
