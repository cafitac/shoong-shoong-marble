from app.chance_card.abstract import ChanceCard

# 방패 카드
# 공격 카드 1회 무효화(통행료는 정상)
class ShieldCard(ChanceCard):
    def __init__(self):
        self.name = "방패 카드"
        self.description = "공격 카드 1회 무효화"

    def use(self):
        # 공격 1회 무효화
        return True
