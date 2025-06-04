from app.board_space.abstract import BoardSpace
from app.player.impl import Player


class TourSpace(BoardSpace):

    def on_land(self, player: Player):
        print(f"{player}님이 관광지에 도착했습니다. 관광지를 방문합니다.")

        

        pass
