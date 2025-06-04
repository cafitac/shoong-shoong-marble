from app.chance_card.abstract import ChanceCard, ChanceCardType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game

# 축제(올림픽) 개최
# 내 현재 도시에 올림픽 마크 설치 → 해당 통행료 ×2 (중첩 불가)
class FestivalCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "축제 개최", "즉시 내 현재 도시에 축제 마크 설치 > 해당 통행료 x 2 (중첩 불가)")

    def use(self, game: 'Game'):
        player = game.get_current_player()  # 현재 플레이어
        selected_space = game.get_board().get_space(1) # TODO: 지역 선택

        for space in game.get_board().get_spaces(): # 모든 도시 축제 해제
            space.set_festival(False)
        selected_space.set_festival(True) # 지정한 도시 축제 지정

        print(f"{player.get_name()}이 {selected_space._name}에 축제 지정")
