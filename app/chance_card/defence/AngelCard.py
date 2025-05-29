from app.chance_card.abstract import ChanceCard

# 천사 카드
# ① 모든 공격 카드 완전 무효화 1회 + ② 통행료 0 원 1회
class AngelCard(ChanceCard):
    def __init__(self):
        self.name = "천사 카드"
        self.description = "모든 공격 카드 무효화 1회 or 통행료 0 원 1회"
        #self.type = type # 무효화 or 통행료 0원

    def use(self):
        return True
