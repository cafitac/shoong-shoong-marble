from app.chance_card.abstract import ChanceCard, ChanceCardType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game

# 강제 도시 매각
# 지정한 상대 도시 1곳 즉시 매각(건물 파괴)
# 랜드마크는 공격 대상에서 제외
class ForcedCitySaleCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "강제 도시 매각", "지정한 상대 도시 1곳 즉시 매각 (랜드마크 제외)")

    def use(self, game: 'Game'):
        target_city = game.get_board().get_city(1)  # 상대 도시

        if target_city.get_owner() is None:         # 소유 땅 없음
            return False
        elif target_city.get_building().is_maxed(): # 랜드마크 제외
            return False

        print(f"{target_city._owner._name}의 {target_city._name}이 매각됨")

        target_city.set_owner(None) # 상대의 도시 소유권 제거
        target_city.get_building()._level = 0

        return True
