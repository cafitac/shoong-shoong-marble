from app.board.impl import Board
from app.game import TurnManager
from app.player.impl import Player


class Game:
    board: Board
    players: list[Player]
    turn_manager: TurnManager
