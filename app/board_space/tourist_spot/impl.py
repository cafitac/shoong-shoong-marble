from typing import Optional

from app.board_space.abstract import BoardSpace, SpaceColor
from app.board_space.land_result import LandResult
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
        #print(f"{player}님이 세계여행에 도착했습니다. 10만 마블을 지불하고 세계여행을 할 수 있습니다.")
        #print("다음 자신의 차례에 주사위를 던지지 않고 원하는 지역으로 바로 이동할 수 있습니다.")

        travel_fee = Money(100)
        if player.get_cash() >= travel_fee:
            player.spend(travel_fee)
            setattr(player, "world_travel_ticket", True)
            #print("세계여행권을 획득했습니다!")
            return LandResult(
                message="세계여행권을 획득했습니다!\n 10만 마블을 지불하고 세계여행을 할 수 있습니다.\n다음 자신의 차례에 주사위를 던지지 않고 원하는 지역으로 바로 이동할 수 있습니다.",
                actions=["OK"],
                callback=lambda choice: None
            )
        else:
            #print("현금이 부족하여 세계여행을 할 수 없습니다.")
            return LandResult(
                message="현금이 부족하여 세계여행을 할 수 없습니다.",
                actions=["OK"],
                callback=lambda choice: None
            )

    def use_world_travel_ticket(self, player: Player):
        def handle_destination_input(seq: str):
            try:
                print("목적지 : " + seq)
                #TODO: 플레이어 이동
                setattr(player, "world_travel_ticket", False)
                return None
            except ValueError:
                return LandResult(
                    message="잘못된 입력입니다. 숫자를 입력해주세요.\n이동할 땅 번호를 입력:",
                    actions=["OK"],
                    callback=handle_destination_input,
                    is_prompt=True
                )

        return LandResult(
            message="세계여행권을 사용합니다.\n이동할 땅 번호를 입력:",
            actions=["OK"],
            callback=handle_destination_input,
            is_prompt=True
        )
