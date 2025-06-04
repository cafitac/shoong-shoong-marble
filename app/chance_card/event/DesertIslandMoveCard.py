from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.game.impl import Game

# 무인도 이동
# 즉시 무인도로 이동(자신에게 불리)
class DesertIslandMoveCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "무인도 이동", "즉시 무인도로 이동")

    def use(self, game: Game):
        player = game.get_current_player()                      # 현재 플레이어
        island_space = game.get_board().get_island()            # 무인도 위치
        game.get_position_manager().teleport(player, island_space.get_seq()) # 플레이어 무인도로 이동
        player.go_to_island()           # 플레이어 무인도 상태 처리

        print(f"{player.get_name()} 무인도로 이동")

        return True
