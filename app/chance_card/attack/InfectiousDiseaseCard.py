from app.board_space.abstract import SpaceColor
from app.board_space.property.impl import AttackEffectType
from app.chance_card.abstract import ChanceCard, ChanceCardType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game

# 전염병
# 대상 색상 도시 통행료 ½로 감소 (랜드마크 면역)
class InfectiousDiseaseCard(ChanceCard):
    def __init__(self, duration: int = 3):
        super().__init__(ChanceCardType.INSTANT, "전염병", "대상 색상 도시 통행료 1/2로 감소 (랜드마크 제외)")
        self.duration = duration
        self.value = 0.5

    def use(self, game: 'Game'):
        target_color = SpaceColor.NONE  # 대상 색상
        affected_city = [
            space for space in game.get_board().get_spaces()
            if space.get_color() == target_color and space.get_building().is_maxed() != True
        ]  # 대상 색상의 도시 (랜드마크 제외)

        for city in affected_city:
            city.set_attack_effect(AttackEffectType.INFECTIOUS_DISEASE, self.duration, self.value)  # 전염병 상태 설정

        print(f"{target_color}색 도시 전염병")
