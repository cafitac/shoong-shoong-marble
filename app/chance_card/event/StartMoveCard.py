from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.game.impl import Game

# 출발지 이동
# START 칸으로 이동 + 월급 수령
class StartMoveCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "출발지 이동", "즉시 START 칸으로 이동")

    def use(self, game: Game):
        player = game.get_current_player()  # 현재 플레이어
        start_space = game.get_board().get_city(0) #.get_start() # 시작 지점
        game.get_position_manager().teleport(player, start_space.get_seq())  # 플레이어 시작 지점 이동

        print(f"{player.get_name()} 시작 지점 이동")

