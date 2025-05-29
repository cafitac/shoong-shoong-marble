from app.chance_card.abstract import ChanceCard

# 정전
# 지정 도시 통행료 0 원(일정 턴)
class BlackoutCard(ChanceCard):
    def __init__(self, target_city_id: int, duration: int):
        self.name = "정전"
        self.description = "지정 도시 통행료 0 원"
        self.target_city_id = target_city_id
        self.duration = duration

    def use(self):
        # 랜드마크일 경우
        if False:
            return False

        # 정전 효과 적용

        return True
