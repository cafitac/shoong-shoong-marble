from typing import Tuple

from app.chance_card.abstract import ChanceCard
from app.money.impl import Money


class Player:
    _idx: int
    _name: str
    _asset: Money = Money.zero()
    _cash: Money = Money.zero()
    _turns_to_wait: int = 0
    _on_island: bool = False
    _color: Tuple[int, int, int]
    _card: ChanceCard = None
    _world_travel_ticket = False

    # 미리 정의된 플레이어 색상들
    PLAYER_COLORS = [
        (255, 0, 0),  # 빨간색
        (0, 0, 255),  # 파란색
        (0, 255, 0),  # 초록색
        (255, 255, 0),  # 노란색
    ]

    def __init__(self, idx: int, name: str) -> None:
        self._idx = idx
        self._name = name
        self._color = self.PLAYER_COLORS[idx % len(self.PLAYER_COLORS)]
        self._cash = Money(1000)

    def __str__(self) -> str:
        color_names = {
            (255, 0, 0): "빨간색",
            (0, 0, 255): "파란색",
            (0, 255, 0): "초록색",
            (255, 255, 0): "노란색"
        }
        return f"{color_names[self._color]} {self._idx}번 플레이어({self._name})"

    def get_idx(self) -> int:
        return self._idx

    def get_name(self) -> str:
        return self._name

    def get_asset(self) -> Money:
        return self._cash

    def get_cash(self) -> Money:
        return self._cash

    def spend(self, amount: Money) -> None:
        self._cash = self._cash - amount

    def is_turn_blocked(self) -> bool:
        return self._turns_to_wait > 0

    def turn_blocked(self, count: int = 3) -> None:
        self._turns_to_wait += count

    def next_turn(self) -> None:
        self._turns_to_wait -= 1

    def go_to_island(self, turns: int = 3):
        self._on_island = True
        self._turns_to_wait = turns

    def leave_island(self):
        self._on_island = False
        self._turns_to_wait = 0

    def is_on_island(self) -> bool:
        return self._on_island

    def receive(self, amount: Money):
        self._cash = self._cash + amount

    def get_color(self) -> Tuple[int, int, int]:
        return self._color

    def get_card(self) -> ChanceCard:
        return self._card

    def set_card(self, card: ChanceCard) -> None:
        self._card = card
