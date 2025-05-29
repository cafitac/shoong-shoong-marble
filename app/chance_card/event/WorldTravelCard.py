from app.chance_card.abstract import ChanceCard

# 세계여행 초대장
# 원하는 도시/관광지/출발지로 즉시 이동 (통행료·축제·올림픽 노리기)
class WorldTravelCard(ChanceCard):
    def __init__(self):
        self.name = "세계여행 초대장"
        self.description = "원하는 도시/관광지/출발지로 즉시 이동"

    def use(self):
        # 플레이어 이동
        return True
