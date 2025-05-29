from app.chance_card.abstract import ChanceCard

# 강제 징수
# 모두 국세청으로 이동·세금 지불
class ForceTaxCard(ChanceCard):
    def __init__(self):
        self.name = "강제 징수"
        self.description = "모두 국세청으로 이동, 세금 지불"

    def use(self):
        tax_position = 0

        # 국세청 이동
        # for player in players:
        #     player.move(tax_position)

        return True
