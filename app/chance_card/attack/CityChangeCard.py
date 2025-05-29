from app.chance_card.abstract import ChanceCard

# 도시 체인지
# 내 도시 1곳 ↔ 상대 도시 1곳 강제 교환
# 랜드마크는 공격 대상에서 제외
class CityChangeCard(ChanceCard):
    def __init__(self, my_city_id: int, target_city_id: int):
        self.name = "도시 체인지"
        self.description = "내 도시 1곳과 상대 도시 1곳 강제 교환"
        self.my_city_id = my_city_id
        self.target_city_id = target_city_id

    def use(self):
        # 랜드마크일 경우
        if False:
            return False

        # 도시 교환
        return True
