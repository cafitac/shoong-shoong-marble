from app.chance_card.abstract import ChanceCard

# 외계인 침공
# 대상 색상의 모든 도시 통행료 0 원 & 건물 기능 정지 (랜드마크는 면역)
class AlienInvasionCard(ChanceCard):
    def __init__(self, target_color: str):
        self.name = "외계인 침공"
        self.description = "대상 색상의 모든 도시 통행료 0 원 & 건물 기능 정지 (랜드마크 제외)"
        self.target_color = target_color

    def use(self):
        # 색상?
        affected_city = [] # 대상 색상의 도시 (랜드마크 제외)
        for city in affected_city:
            # 통행료 0원
            # 건물 기능 정지
            continue
        return True
