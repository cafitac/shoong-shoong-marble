from app.chance_card.abstract import ChanceCard

# 출발지 이동
# START 칸으로 이동 + 월급 수령
class StartMoveCard(ChanceCard):
    def __init__(self):
        self.name = "출발지 이동"
        self.description = "START 칸으로 이동 + 월급 수령"

    def use(self):
        # 플레이어 출발지로 이동
        return True
