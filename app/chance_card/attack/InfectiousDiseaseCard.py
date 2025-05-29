from app.chance_card.abstract import ChanceCard

# 전염병
# 대상 색상 도시 통행료 ½로 감소 (랜드마크 면역)
class InfectiousDiseaseCard(ChanceCard):
    def __init__(self, target_color: str):
        self.name = "전염병"
        self.description = "대상 색상 도시 통행료 1/2로 감소 (랜드마크 제외)"
        self.target_color = target_color

    def use(self):
        # 색상?
        affected_city = []  # 대상 색상의 도시 (랜드마크 제외)
        for city in affected_city:
            # 통행료 1/2
            continue
        return True
