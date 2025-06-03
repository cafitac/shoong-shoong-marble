from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.game.impl import Game

# 세계여행 초대장
# 원하는 도시/관광지/출발지로 즉시 이동 (통행료·축제·올림픽 노리기)
class WorldTravelCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "세계여행 초대장", "원하는 도시/관광지/출발지로 즉시 이동")

    def use(self, game: Game):
        player = game.get_current_player()  # 현재 플레이어
        travel_space = game.get_board().get_city(0) # 원하는 위치
        game.get_position_manager().teleport(player, travel_space.get_seq())  # 플레이어 이동

        print(f"{player.get_name()}, {travel_space._name}으로 이동")
