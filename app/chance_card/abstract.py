from abc import ABC, abstractmethod
from enum import Enum
from typing import Any
from app.game.impl import Game

class ChanceCardType(Enum):
    INSTANT = 0
    KEEP = 1

class ChanceCard(ABC):
    def __init__(self, card_type: ChanceCardType, name: str, description: str):
        self.card_type = card_type
        self.name = name
        self.description = description

    @abstractmethod
    def use(self, game: Game) -> Any:
        ...
