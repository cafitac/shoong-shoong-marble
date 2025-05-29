from app.chance_card.abstract import ChanceCard

# 무인도 이동
# 즉시 무인도로 이동(자신에게 불리)
class DesertIslandMoveCard(ChanceCard):
    def __init__(self):
        self.name = "세계여행 초대장"
        self.description = "즉시 무인도로 이동"

    def use(self):
        # 플레이어 무인도 이동
        return True
