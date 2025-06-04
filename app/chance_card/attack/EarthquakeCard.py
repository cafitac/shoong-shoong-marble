from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.game.impl import Game

# 지진
# 건물 단계 1 단계씩 파괴
# 랜드마크는 공격 대상에서 제외
class EarthquakeCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "지진", "건물 단계 1 단계씩 파괴 (랜드마크 제외)")

    def use(self, game: Game):
        target_city = game.get_board().get_city(1) # 지정 도시

        # 랜드마크일 경우
        if target_city.get_building().is_maxed():
            return False

        # 건물 단계 1단계 하락
        current_level = target_city.get_building().get_level()
        if current_level > 1:
            target_city.get_building()._level = current_level - 1
            print(f"{target_city.get_name()}의 건물 단계가 1단계 파괴")

        return True
