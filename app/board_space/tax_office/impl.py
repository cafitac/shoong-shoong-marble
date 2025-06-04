from typing import Optional

from app.board_space.abstract import BoardSpace, SpaceColor
from app.money.impl import Money
from app.player.impl import Player
from app.board_space.property.impl import PropertySpace


class TaxOfficeSpace(BoardSpace):
    def __init__(self, seq: int, name: str, board_spaces, color: Optional[SpaceColor] = None):
        super().__init__(seq, name, color)
        self.board_spaces = board_spaces

    def on_land(self, player: Player):
        print(f"{player}님이 국세청에 도착했습니다. 세금을 납부해야 합니다.")

        # 1. 플레이어가 소유한 모든 PropertySpace 찾기
        player_properties = [
            # TODO : property_data 연동 필요
            space for space in self.board_spaces
            if isinstance(space, PropertySpace) and space._owner == player
        ]

        # 2. 각 건물의 가치 합산
        total_value = sum(prop._building.get_price() for prop in player_properties)

        # 3. 세금 계산
        tax = Money(int(total_value * 0.05))

        # 4. 소지금 확인 및 차감
        if player.get_cash() >= tax:
            player.spend(tax)
            print(f"전체 건물 가치: {total_value}원, 세금(5%): {tax}원을 납부했습니다.")
        else:
            print(f"소지금이 부족합니다! (보유 현금: {player.get_cash()}원, 세금: {tax}원)")
            # TODO : 추가 파산 처리, 자산 매각 등 로직 구현
