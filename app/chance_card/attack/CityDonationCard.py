from app.chance_card.abstract import ChanceCard

# 도시 기부
# 내 도시 1곳을 선택한 상대에게 무상 양도
class CityDonationCard(ChanceCard):
    def __init__(self, my_city_id: int, target_player_id: int):
        self.name = "도시 기부"
        self.description = "내 도시 1곳을 선택한 상대에게 무상 양도"
        self.my_city_id = my_city_id
        self.target_player_id = target_player_id

    def use(self):
        # 도시 소유권을 target_player로 설정
        
        return True
