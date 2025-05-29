from app.chance_card.abstract import ChanceCard

# 황사
# 지정 도시 통행료 ½로 하락
class YellowDustCard(ChanceCard):
    def __init__(self, target_city_id: str):
        self.name = "황사"
        self.description = "지정 도시 통행료 1/2로 하락"
        self.target_city_id = target_city_id

    def use(self):
        # 통행료 1/2
        return True
