from app.chance_card.abstract import ChanceCard

# 무인도 탈출
# 무인도에서 즉시 탈출
class IslandEscapeCard(ChanceCard):
    def __init__(self):
        self.name = "무인도 탈출"
        self.description = "무인도에서 즉시 탈출"

    def use(self):
        # 무인도 탈출
        return True
