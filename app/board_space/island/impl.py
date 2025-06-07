from app.board_space.abstract import BoardSpace
from app.board_space.land_result import LandResult
from app.player.impl import Player


class IslandSpace(BoardSpace):

    def on_land(self, player: Player):
        #print(f"{player}님이 무인도에 도착했습니다. 지금부터 3턴 동안 쉬어야 합니다.")
        #print("단, 주사위 더블이 나오는 경우에는 즉시 섬에서 탈출할 수 있습니다.")
        # 무인도 도착 시
        player.go_to_island(3)

        return LandResult(
            f"{player.get_name()}님이 무인도에 도착했습니다. 지금부터 3턴 동안 쉬어야 합니다.\n"
            "단, 주사위 더블이 나오는 경우에는 즉시 섬에서 탈출할 수 있습니다."
            ,
            ["OK"],
            lambda _: None
        )
