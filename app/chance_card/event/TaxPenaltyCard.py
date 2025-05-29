from app.chance_card.abstract import ChanceCard

# 세금(강제 징수)
# 국세청으로 이동 후 세금 납부(자산 비례)
class TaxPenaltyCard(ChanceCard):
    def __init__(self):
        self.name = "세금(강제 징수)"
        self.description = "국세청으로 이동 후 세금 납부"

    def use(self):
        # 국세청으로 이동
        return True
