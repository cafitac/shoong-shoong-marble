from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.board_space.property.impl import AttackEffectType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game

# 정전
# 지정 도시 통행료 0 원(일정 턴)
class BlackoutCard(ChanceCard):
    def __init__(self, duration:int = 3):
        super().__init__(ChanceCardType.INSTANT, "정전", "지정 도시 통행료 0 원")
        self.duration = duration
        self.value = 0.0

    def use(self, game: 'Game'):
        target_city = game.get_board().get_city(1) # 지정 도시

        # 랜드마크일 경우
        if target_city.get_building().is_maxed():
            return False

        target_city.set_attack_effect(AttackEffectType.BLACK_OUT, self.duration, self.value)  # 황사 상태 설정

        print(f"{target_city._name} : 정전")
        return True