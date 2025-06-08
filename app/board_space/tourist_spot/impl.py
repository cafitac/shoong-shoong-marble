from typing import Optional

from app.board_space.abstract import BoardSpace
from app.board_space.land_result import LandResult
from app.money.impl import Money
from app.player.impl import Player


class TouristSpotSpace(BoardSpace):
    def __init__(self, seq: int, name: str, price: Money):
        super().__init__(seq, name)
        self._name = name
        self._owner: Optional[Player] = None
        self._base_price = price

    def on_land(self, player: Player):
        print(f"{player}님이 관광지에 도착했습니다. 관광지를 방문합니다.")
        if self._owner is None:
            def handle_choice(choice: str):
                if choice == "BUILD":
                    self.buy_land(player)
                return None

            return LandResult(
                f"{self.get_name()}에 도착했습니다.\n구매하시겠습니까?",
                ["BUILD", "PASS"],
                handle_choice
            )
        elif self._owner == player:
            #self.upgrade_building(player)
            return None
        else:
            toll = self._base_price

            def handle_toll_payment(choice: str):
                if player.get_cash().amount >= toll.amount:
                    player.spend(toll)
                    self._owner.receive(toll)
                    return None
                else:
                    print(f"{player.get_name()}님이 통행료를 낼 수 없습니다.")
                    return LandResult(
                        f"{player.get_name()}님의 잔액이 부족하여 통행료를 낼 수 없습니다.\n(추가 파산처리 필요)",
                        ["OK"],
                        lambda _: None
                    )

            return LandResult(
                f"{self.get_name()}은(는) {self._owner.get_name()}의 소유입니다.\n통행료 {toll.amount}만원을 지불합니다.",
                ["OK"],
                handle_toll_payment
            )

    def buy_land(self, player: Player):
        price = self._base_price
        if player.get_cash().amount >= price.amount:
            player.spend(price)
            self._owner = player
            print(f"{player}님이 {self._name}을 구매했습니다!")
        else:
            print(f"{player}님은 돈이 부족하여 {self._name}을 구매할 수 없습니다.")

    def get_owner(self) -> Player:
        return self._owner