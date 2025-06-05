from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.board_space.property.impl import AttackEffectType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game

# 황사
# 지정 도시 통행료 ½로 하락
class YellowDustCard(ChanceCard):
    def __init__(self, duration: int = 3):
        super().__init__(ChanceCardType.INSTANT, "황사", "지정 도시 통행료 1/2로 하락")
        self.duration = duration
        self.value = 0.5

    def use(self, game: 'Game'):
        target_city = game.get_board().get_space(1) # 지정 도시
        target_city.set_attack_effect(AttackEffectType.YELLOW_DUST, self.duration, self.value)  # 황사 상태 설정

        print(f"{target_city._name} : 황사")
