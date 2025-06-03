from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.game.impl import Game

# 세금(강제 징수)
# 국세청으로 이동 후 세금 납부(자산 비례)
class TaxPenaltyCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "세금(강제 징수)", "즉시 국세청으로 이동 후 세금 납부")

    def use(self, game: Game):
        player = game.get_current_player()  # 현재 플레이어
        tax_space = game.get_board().get_city(0) #.get_tax_penalty() # 국세청
        game.get_position_manager().teleport(player, tax_space.get_seq())  # 플레이어 이동

        print(f"{player.get_name()} 국세청 이동")