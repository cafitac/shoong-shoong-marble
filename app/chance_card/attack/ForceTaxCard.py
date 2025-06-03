from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.game.impl import Game

# 강제 징수
# 모두 국세청으로 이동·세금 지불
class ForceTaxCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "강제 징수", "모두 국세청으로 이동, 세금 지불")

    def use(self, game: Game):
        tax_space = game.get_board().get_city(0) #.get_tax_penalty() # 국세청

        # 국세청 이동
        for player in game.get_players():
            game.get_position_manager().teleport(player, tax_space.get_seq())  # 플레이어 이동

        print("모두 국세청으로 이동")