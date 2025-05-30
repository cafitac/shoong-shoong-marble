from typing import Optional
from app.board_space.abstract import BoardSpace, SpaceColor
from app.player.impl import Player
from app.money.impl import Money

class Building:
    def __init__(self):
        self._level = 0  # 0: 없음, 1: 별장, 2: 빌딩, 3: 호텔, 4: 랜드마크
        self._base_price: Optional[Money] = None

    def set_price(self, base_price: Money):
        self._base_price = base_price

    def get_price(self) -> Money:
        return self._base_price if self._base_price else Money.zero()

    def get_upgrade_cost(self) -> Money:
        return self.get_price() / 2

    def upgrade(self):
        if self._level < 4:
            self._level += 1

    def get_level(self) -> int:
        return self._level

    def is_maxed(self) -> bool:
        return self._level >= 4

    def can_build_landmark(self) -> bool:
        return self._level == 3


class PropertySpace(BoardSpace):
    def __init__(
        self,
        seq: int,
        name: str,
        price: Money,
        color: Optional[SpaceColor] = None
    ):
        super().__init__(seq, color)
        self._name = name
        self._owner: Optional[Player] = None
        self._building = Building()
        self._building.set_price(price)

    def on_land(self, player: Player):
        price = self._building.get_price()
        if self._owner is None:
            if player.get_cash() >= price:
                player.spend(price)
                self._owner = player
                self._building.upgrade()
                print(f"{player}님이 {self._name}에 별장을 건설했습니다!")
            else:
                print(f"{player}님은 돈이 부족하여 {self._name}을 구매할 수 없습니다.")

        elif self._owner == player:
            cost = self._building.get_upgrade_cost()
            level = self._building.get_level()

            if level == 1:
                if player.get_cash() >= cost:
                    player.spend(cost)
                    self._building.upgrade()
                    print(f"{player}님이 {self._name}에 빌딩을 건설했습니다!")
                else:
                    print("빌딩 건설 비용이 부족합니다.")

            elif level == 2:
                if player.get_cash() >= cost:
                    player.spend(cost)
                    self._building.upgrade()
                    print(f"{player}님이 {self._name}에 호텔을 건설했습니다!")
                else:
                    print("호텔 건설 비용이 부족합니다.")

            elif level == 3:
                if self._building.can_build_landmark():
                    if player.get_cash() >= cost:
                        player.spend(cost)
                        self._building.upgrade()
                        print(f"{player}님이 {self._name}에 랜드마크를 건설했습니다!")
                    else:
                        print("랜드마크 건설 비용이 부족합니다.")
                else:
                    print("조건을 만족하지 않아 랜드마크를 건설할 수 없습니다.")

            elif self._building.is_maxed():
                print(f"{self._name}은 이미 랜드마크까지 건설된 상태입니다!")

        else:
            print(f"{self._name}은 {self._owner}님의 소유입니다.")

