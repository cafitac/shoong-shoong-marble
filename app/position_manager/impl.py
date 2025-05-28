from app.board.impl import Board
from app.board_space.abstract import BoardSpace
from app.player.impl import Player


class PositionManager:
    _board: Board
    _positions: dict[Player, int]

    def __init__(self, board: Board, players: list[Player]):
        self._board = board
        self._positions = {p: 0 for p in players}

    def get_location(self, player: Player) -> BoardSpace:
        idx = self._positions[player]
        return self._board._spaces[idx]

    def move(self, player: Player, steps: int) -> BoardSpace:
        new_idx = (self._positions[player] + steps) % len(self._board._spaces)
        self._positions[player] = new_idx
        return self.get_location(player)

    def teleport(self, player: Player, destination_idx: int) -> None:
        self._positions[player] = destination_idx
