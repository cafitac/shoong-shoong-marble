import csv
from enum import Enum
from typing import Optional
from app.board_space.abstract import BoardSpace, SpaceColor
from app.player.impl import Player
from app.money.impl import Money

class Building:
    def __init__(self, base_price: Money):
        self._level = 0
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

    def get_acquisition_cost(self) -> Money:
        return self._base_price * 2

    def calculate_toll(self) -> Money:
        return self._base_price * (0.2 + 0.2 * self._level)


class PropertySpace(BoardSpace):
    def __init__(self, seq: int, name: str, price: Money, color: Optional[SpaceColor] = None):
        super().__init__(seq, color)
        self._name = name
        self._owner: Optional[Player] = None
        self._building = Building(price)

    def on_land(self, player: Player):
        if self._owner is None:
            self.buy_land(player)
        elif self._owner == player:
            self.upgrade_building(player)
        else:
            self.pay_toll(player)
            self.offer_acquisition(player)

    def buy_land(self, player: Player):
        price = self._building.get_price()
        if player.get_cash() >= price.amount:
            player.spend(price)
            self._owner = player
            self._building.upgrade()
            print(f"{player}님이 {self._name}에 별장을 건설했습니다!")
        else:
            print(f"{player}님은 돈이 부족하여 {self._name}을 구매할 수 없습니다.")

    def upgrade_building(self, player: Player):
        cost = self._building.get_upgrade_cost()
        level = self._building.get_level()
        if level == 1:
            self._try_upgrade(player, cost, "빌딩")
        elif level == 2:
            self._try_upgrade(player, cost, "호텔")
        elif level == 3:
            if self._building.can_build_landmark():
                self._try_upgrade(player, cost, "랜드마크")
            else:
                print("조건을 만족하지 않아 랜드마크를 건설할 수 없습니다.")
        elif self._building.is_maxed():
            print(f"{self._name}은 이미 랜드마크까지 건설된 상태입니다!")

    def _try_upgrade(self, player: Player, cost: Money, building_name: str):
        if player.get_cash() >= cost.amount:
            player.spend(cost)
            self._building.upgrade()
            print(f"{player}님이 {self._name}에 {building_name}을 건설했습니다!")
        else:
            print(f"{building_name} 건설 비용이 부족합니다.")

    def pay_toll(self, player: Player):
        toll = self._building.calculate_toll()
        if player.get_cash() >= toll.amount:
            player.spend(toll)
            self._owner.receive(toll)
            print(f"{player}님이 {self._name}의 통행료 {toll}를 지불했습니다!")
        else:
            print(f"{player}님이 통행료를 지불할 금액이 부족합니다. (파산처리 등 추가 가능)")

    def offer_acquisition(self, player: Player):
        acquisition_cost = self._building.get_acquisition_cost()
        print(f"{self._name}은 {self._owner}님 소유입니다. 인수 금액: {acquisition_cost.amount}만원")
        response = input("인수하시겠습니까? (y/n): ").strip().lower()
        if response == "y":
            self.purchase_from_owner(player)
        else:
            print("인수를 포기했습니다.")

    def purchase_from_owner(self, player: Player):
        acquisition_cost = self._building.get_acquisition_cost()
        if player.get_cash() >= acquisition_cost.amount:
            player.spend(acquisition_cost)
            self._owner = player
            print(f"{player}님이 {self._name}을 인수했습니다!")
        else:
            print("인수 비용이 부족합니다.")

    def get_owner(self) -> Optional[Player]:
        return self._owner


# 건물 가격 정보 연동 로직
def load_property_data(file_path: str):
    properties = []
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            seq = int(row['번호'])
            name = row['건물명']
            price = Money(int(row['가격(만원)']))
            property_space = PropertySpace(seq, name, price)
            properties.append(property_space)
    return properties


class AttackEffectType(Enum):
    NONE = 0
    YELLOW_DUST = 1
    INFECTIOUS_DISEASE = 2
    ALIEN_INVASION = 3
    BLACK_OUT = 4


class PropertySpace(BoardSpace):
    def __init__(self, seq: int, name: str, price: Money, color: Optional[SpaceColor] = None):
        super().__init__(seq, name, color)
        self._name = name
        self._owner: Optional[Player] = None
        self._building = Building(price)
        self.olympic = False

        # 공격 카드 상태
        self._attack_effect_type = AttackEffectType.NONE
        self._attack_effect_value: float = 1.0
        self._attack_effect_duration: int = 0

        # 이벤트 카드 상태
        self._is_festival = False

    def on_land(self, player: Player):
        if self._owner is None:
            self.buy_land(player)
        elif self._owner == player:
            self.upgrade_building(player)
        else:
            self.pay_toll(player)
            self.offer_acquisition(player)

    def buy_land(self, player: Player):
        price = self._building.get_price()
        if player.get_cash().amount >= price.amount:
            player.spend(price)
            self._owner = player
            self._building.upgrade()
            print(f"{player}님이 {self._name}에 별장을 건설했습니다!")
        else:
            print(f"{player}님은 돈이 부족하여 {self._name}을 구매할 수 없습니다.")

    def upgrade_building(self, player: Player):
        cost = self._building.get_upgrade_cost()
        level = self._building.get_level()
        if level == 1:
            self._try_upgrade(player, cost, "빌딩")
        elif level == 2:
            self._try_upgrade(player, cost, "호텔")
        elif level == 3:
            if self._building.can_build_landmark():
                self._try_upgrade(player, cost, "랜드마크")
            else:
                print("조건을 만족하지 않아 랜드마크를 건설할 수 없습니다.")
        elif self._building.is_maxed():
            print(f"{self._name}은 이미 랜드마크까지 건설된 상태입니다!")

    def _try_upgrade(self, player: Player, cost: Money, building_name: str):
        if player.get_cash().amount >= cost.amount:
            player.spend(cost)
            self._building.upgrade()
            print(f"{player}님이 {self._name}에 {building_name}을 건설했습니다!")
        else:
            print(f"{building_name} 건설 비용이 부족합니다.")

    def pay_toll(self, player: Player):
        toll = self._building.calculate_toll()
        if player.get_cash().amount >= toll.amount:
            player.spend(toll)
            self._owner.receive(toll)
            print(f"{player}님이 {self._name}의 통행료 {toll}를 지불했습니다!")
        else:
            print(f"{player}님이 통행료를 지불할 금액이 부족합니다. (파산처리 등 추가 가능)")

    def offer_acquisition(self, player: Player):
        acquisition_cost = self._building.get_acquisition_cost()
        print(f"{self._name}은 {self._owner}님 소유입니다. 인수 금액: {acquisition_cost.amount}만원")
        response = input("인수하시겠습니까? (y/n): ").strip().lower()
        if response == "y":
            self.purchase_from_owner(player)
        else:
            print("인수를 포기했습니다.")

    def purchase_from_owner(self, player: Player):
        acquisition_cost = self._building.get_acquisition_cost()
        if player.get_cash().amount >= acquisition_cost.amount:
            player.spend(acquisition_cost)
            self._owner = player
            print(f"{player}님이 {self._name}을 인수했습니다!")
        else:
            print("인수 비용이 부족합니다.")

    # 공격 카드 관련 함수
    def set_attack_effect(self, type: AttackEffectType, duration: int, value: float):
        self._attack_effect_type = type
        self._attack_effect_duration = duration
        self._attack_effect_value = value

    def reduce_attack_effect_duration(self):
        if self._attack_effect_duration > 0:
            self._attack_effect_duration -= 1
            if self._attack_effect_duration == 0:
                self.clear_attack_effect()

    def clear_attack_effect(self):
        self._attack_effect_type = AttackEffectType.NONE
        self._attack_effect_value = 1.0
        self._attack_effect_duration = 0

    def set_festival(self, is_festival):
        self._is_festival = is_festival

    def get_owner(self) -> Optional[Player]:
        return self._owner

    def get_building(self) -> Building:
        return self._building

    def get_color(self) -> SpaceColor:
        return self._color
