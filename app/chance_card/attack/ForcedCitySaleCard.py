from app.chance_card.abstract import ChanceCard

# 강제 도시 매각
# 지정한 상대 도시 1곳 즉시 매각(건물 파괴)
# 랜드마크는 공격 대상에서 제외
class ForcedCitySaleCard(ChanceCard):
    def __init__(self, target_city_id: int):
        self.name = "강제 도시 매각"
        self.description = "지정한 상대 도시 1곳 즉시 매각 (랜드마크 제외)"
        self.target_city_id = target_city_id

    def use(self):
        # 랜드마크일 경우
        if False:
            return False

        # 도시 매각
        # 상대의 도시 소유권 제거
        return True
