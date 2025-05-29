from app.chance_card.abstract import ChanceCard

# 지진
# 건물 단계 1 단계씩 파괴
# 랜드마크는 공격 대상에서 제외
class EarthquakeCard(ChanceCard):
    def __init__(self, target_city_id: str):
        self.name = "지진"
        self.description = "건물 단계 1 단계씩 파괴 (랜드마크 제외)"
        self.target_city_id = target_city_id

    def use(self):
        # 랜드마크일 경우
        if False:
            return False

        # 건물 단계 1단계 하락

        return True
