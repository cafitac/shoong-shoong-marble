from app.board.impl import Board
from app.board_space.abstract import BoardSpace, SpaceColor
from app.board_space.island.impl import IslandSpace
from app.dice.dices import Dices
from app.player.impl import Player
from app.position_manager.impl import PositionManager
from app.turn_manager.impl import TurnManager


class Game:
    _board: Board
    _players: list[Player]
    _turn_manager: TurnManager
    _position_manager: PositionManager
    _dices: Dices

    def __init__(self, players: list[Player]):
        space_1: BoardSpace = IslandSpace(seq=0, color=SpaceColor.LIGHT_GREEN)
        # space_2: BoardSpace = BoardSpace(seq=1, color=SpaceColor.GREEN)
        # space_3: BoardSpace = BoardSpace(seq=2, color=SpaceColor.NONE)

        self._board = Board([space_1])
        self._players = players
        self._turn_manager = TurnManager(self._players)
        self._position_manager = PositionManager(self._board, self._players)
        self._dices = Dices(count=2)

    def get_players(self) -> list[Player]:
        return self._players

    def get_current_player(self) -> Player:
        return self._turn_manager.get_current_player()

    def get_position_by_player(self, player: Player) -> BoardSpace:
        return self._position_manager.get_location(player)

    def get_board(self) -> Board:
        return self._board

    def get_position_manager(self) -> PositionManager:
        return self._position_manager

    def roll_dices(self) -> list[int]:
        return self._dices.roll()

    def draw_board(self) -> None:
        pass
