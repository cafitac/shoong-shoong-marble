from typing import Optional

from app.board_space.abstract import BoardSpace, SpaceColor
from app.money.impl import Money
from app.player.impl import Player


class TouristSpotSpace(BoardSpace):
    def __init__(self, seq: int, name: str, price: Money, color: Optional[SpaceColor] = None):
        super().__init__(seq, name, color)
        self._name = name
        self._owner: Optional[Player] = None
        self._price = price

        # 이벤트 카드 상태
        self._is_festival = False

    def on_land(self, player: Player):
        pass
