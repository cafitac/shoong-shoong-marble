from app.chance_card.abstract import ChanceCard

# 통행료 면제
# 다음 통행료 0 원 1회
class TollFreeCard(ChanceCard):
    def __init__(self):
        self.name = "통행료 면제"
        self.description = "통행료 0 원 1회"

    def use(self):
        # 통행료 0원
        return True
