from app.board_space.tax_office.impl import TaxOfficeSpace
from app.chance_card.abstract import ChanceCard, ChanceCardType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game
# 세금(강제 징수)
# 국세청으로 이동 후 세금 납부(자산 비례)
class TaxPenaltyCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "세금(강제 징수)", "즉시 국세청으로 이동 후 세금 납부")

    def use(self, game: 'Game'):
        player = game.get_turn_manager().get_prev_player()  # 현재 플레이어
        current_index = game.get_position_manager().get_position(player)
        tax_space = game.get_board().get_nearest_space_by_type(current_index, TaxOfficeSpace) # 국세청
        game.get_position_manager().set_position(player, tax_space.get_seq())  # 플레이어 이동

        print(f"{player.get_name()} 국세청 이동")
        return tax_space.on_land(player)