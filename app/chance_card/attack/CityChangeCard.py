from app.chance_card.abstract import ChanceCard, ChanceCardType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game

# 도시 체인지
# 내 도시 1곳 ↔ 상대 도시 1곳 강제 교환
# 랜드마크는 공격 대상에서 제외
class CityChangeCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "도시 체인지", "내 도시 1곳과 상대 도시 1곳 강제 교환 (즉시 사용)")

    def use(self, game: 'Game'):
        player = game.get_current_player()  # 현재 플레이어

        my_city = game.get_board().get_city(0) # 내 도시
        target_city = game.get_board().get_city(1) # 상대 도시

        temp_city = my_city
        my_city._owner = target_city.get_owner()
        target_city._owner = temp_city.get_owner()

        print(f"{player.get_name()}이 {my_city._name}을 {target_city._name}으로 교환")
