from app.board_space.abstract import SpaceColor
from app.board_space.property.impl import AttackEffectType
from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.game.impl import Game

# 외계인 침공
# 대상 색상의 모든 도시 통행료 0 원 & 건물 기능 정지 (랜드마크는 면역)
class AlienInvasionCard(ChanceCard):
    def __init__(self, duration: int = 3):
        super().__init__(ChanceCardType.INSTANT, "외계인 침공", "대상 색상의 모든 도시 통행료 0 원 (랜드마크 제외)")
        self.duration = duration
        self.value = 0.0

    def use(self, game: Game):
        target_color = SpaceColor.NONE # 대상 색상
        affected_city = [
            space for space in game.get_board().get_spaces()
            if space.get_color() == target_color and space.get_building().is_maxed() != True
        ] # 대상 색상의 도시 (랜드마크 제외)
        
        for city in affected_city:
            city.set_attack_effect(AttackEffectType.ALIEN_INVASION, self.duration, self.value)  # 외계인 침공 상태 설정

        print(f"{target_color}색 도시 외계인 침공")
