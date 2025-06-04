from typing import Optional

from app.board_space.abstract import BoardSpace, SpaceColor
from app.money.impl import Money
from app.player.impl import Player


class TouristSpotSpace(BoardSpace):
    def __init__(self, seq: int, name: str, price: Money, color: Optional[SpaceColor] = None):
        super().__init__(seq, name, color)
        self._name = name
        self._owner: Optional[Player] = None
        self._price = price

        # 이벤트 카드 상태
        self._is_festival = False

    def on_land(self, player: Player):
        print(f"{player}님이 세계여행에 도착했습니다. 10만 마블을 지불하고 세계여행을 할 수 있습니다.")
        print("다음 자신의 차례에 주사위를 던지지 않고 원하는 지역으로 바로 이동할 수 있습니다.")

        travel_fee = Money(100_000)
        if player.get_cash() >= travel_fee:
            player.spend(travel_fee)
            # TODO : 플레이어에게 세계여행 플래그 부여? (ex: player.world_travel_ticket = True)
            # TODO : 실제 ui 상 세계 여행지 선택 및 이동할 수 있는 로직 구현이 필요합니다.
            setattr(player, "world_travel_ticket", True)
            print("세계여행권을 획득했습니다!")
        else:
            print("현금이 부족하여 세계여행을 할 수 없습니다.")