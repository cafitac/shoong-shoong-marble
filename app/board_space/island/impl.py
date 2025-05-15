from app.board_space.abstract import BoardSpace
from app.player.impl import Player


class IslandSpace(BoardSpace):

    def on_land(self, player: Player):
        pass
