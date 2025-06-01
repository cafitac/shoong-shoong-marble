from app.board_space.abstract import BoardSpace
from app.player.impl import Player


class StartSpace(BoardSpace):

    def on_land(self, player: Player):
        print(f"{player}님이 출발지에 도착했습니다. 보너스를 받습니다!")
        pass
