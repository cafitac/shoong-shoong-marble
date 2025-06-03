from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.game.impl import Game

# 도시 기부
# 내 도시 1곳을 선택한 상대에게 무상 양도
class CityDonationCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "도시 기부", "내 도시 1곳을 선택한 상대에게 무상 양도")

    def use(self, game: Game):
        player = game.get_current_player()  # 현재 플레이어
        selected_space = game.get_board().get_city(1)  # 도시 지정
        target_player = game.get_players()[0] # 플레이어 지정

        selected_space._owner = target_player

        print(f"{player.get_name()}이 {target_player.get_name()}에게 {selected_space._name} 양도")