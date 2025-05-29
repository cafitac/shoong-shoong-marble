from app.chance_card.abstract import ChanceCard

# 올림픽 개최
# 내 현재 도시에 올림픽 마크 설치 → 해당 통행료 ×2 (중첩 불가)
class OlympicCard(ChanceCard):
    def __init__(self):
        self.name = "올림픽 개최"
        self.description = "내 현재 도시에 올림픽 마크 설치 > 해당 통행료 x 2 (중첩 불가)"

    def use(self):
        # 중첩 확인
        if False:
            return False
        # 올림픽 마크 설치 (통행료 2배)
        return True
