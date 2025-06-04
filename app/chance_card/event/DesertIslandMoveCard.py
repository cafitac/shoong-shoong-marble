from app.board_space.island.impl import IslandSpace
from app.chance_card.abstract import ChanceCard, ChanceCardType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game

# 무인도 이동
# 즉시 무인도로 이동(자신에게 불리)
class DesertIslandMoveCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "무인도 이동", "즉시 무인도로 이동")

    def use(self, game: 'Game'):
        player = game.get_current_player()                      # 현재 플레이어
        current_index = game.get_position_manager().get_position(player)
        island_space = game.get_board().get_nearest_space_by_type(current_index, IslandSpace)            # 무인도 위치
        game.get_position_manager().set_position(player, island_space.get_seq()) # 플레이어 무인도로 이동
        player.go_to_island()           # 플레이어 무인도 상태 처리

        print(f"{player.get_name()} 무인도로 이동")

        return True
