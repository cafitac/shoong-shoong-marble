from typing import Tuple, Optional
from app.money.impl import Money
from app.chance_card.abstract import ChanceCard


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
    _position: int = 0
    _lap_count: int = 0  # 보드를 돈 횟수 추적

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
        self._position = 0
        self._lap_count = 0 # 보드를 돈 횟수 추적
        self._spaces: list = []
        self._is_bankrupt = False # 파산 여부

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

    def get_card(self) -> Optional[ChanceCard]:
        return self._card

    def set_card(self, card: ChanceCard) -> None:
        self._card = card

    def get_position(self) -> int:
        return self._position

    def set_position(self, position: int, board_size: int = 32) -> None:
        # 시작점(0)을 지나면 랩 카운트 증가
        if position < self._position and position < board_size:
            self.increase_lap_count()
        self._position = position

    def move_position(self, steps: int, board_size: int = 32) -> None:
        new_position = (self._position + steps) % board_size
        # 시작점(0)을 지나면 랩 카운트 증가
        if new_position < self._position:
            self.increase_lap_count()
        self._position = new_position

    def get_lap_count(self) -> int:
        return self._lap_count

    def increase_lap_count(self) -> None:
        self._lap_count += 1

    def set_lap_count(self, count: int) -> None:
        self._lap_count = count

    def has_world_travel_ticket(self) -> bool:
        return self._world_travel_ticket

    def set_world_travel_ticket(self, has_ticket: bool) -> None:
        self._world_travel_ticket = has_ticket

    def add_space(self, space):
        self._spaces.append(space)

    def remove_space(self, space):
        if space in self._spaces:
            self._spaces.remove(space)

    def get_spaces(self) -> list:
        return self._spaces

    def set_bankrupt(self):
        self._is_bankrupt = True
        for space in self._spaces:
            space._owner = None
            space._building._level = 0
        self._spaces = []
