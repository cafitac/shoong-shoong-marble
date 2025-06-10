import csv
from enum import Enum
from typing import Optional
from app.board_space.abstract import BoardSpace, SpaceColor
from app.board_space.land_result import LandResult
from app.board_space.tourist_spot.impl import TouristSpotSpace
from app.player.impl import Player
from app.money.impl import Money


class BuildingType(Enum):
    """모두의 마블 건물 타입을 나타내는 열거형 클래스입니다."""
    NONE = 0  # 아무것도 건설되지 않은 상태
    VILLA = 1  # 빌라
    BUILDING = 2  # 빌딩
    HOTEL = 3  # 호텔
    LANDMARK = 4  # 랜드마크


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

    def calculate_toll(self, is_festival=False, effect_value=1.0) -> Money:
        toll = self._base_price * (0.2 + 0.2 * self._level)
        if is_festival:
            toll *= 2
        toll *= effect_value
        return toll


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

    def on_land(self, player: Player) -> LandResult:
        # 플레이어의 랩 수에 따라 건설 가능한 건물 옵션 결정
        lap_count = player.get_lap_count()
        available_buildings = []

        if lap_count >= 0:  # 1바퀴째 (시작 포함)
            available_buildings.append("별장")
        if lap_count >= 1:  # 2바퀴째 (시작점 한번 이상 통과)
            available_buildings.append("빌딩")
        if lap_count >= 2:  # 3바퀴째
            available_buildings.append("호텔")
        can_build_landmark = lap_count >= 3  # 4바퀴째부터 랜드마크 가능

        if self._owner is None:
            # 주인이 없는 땅: 랩 수에 따라 건설 가능한 옵션 제공
            options = available_buildings + ["PASS"]

            return LandResult(
                f"{self.get_name()}은(는) 비어있는 땅입니다.\n어떤 건물을 건설하시겠습니까?",
                options,
                lambda choice: self.handle_build_choice(choice, player),
                player=player,
                property=self
            )
        elif self._owner == player:
            # 자신의 소유지: 현재 구매되어있는 곳에서 랩 수에 따라 업그레이드 가능
            level = self._building.get_level()

            if level == 3 and can_build_landmark:  # 호텔까지 구매되어 있고 4바퀴 이상 돌았으면 랜드마크까지 구매 가능
                return LandResult(
                    f"{self.get_name()}에 랜드마크를 건설하시겠습니까?\n"
                    f"비용: {self._building.get_upgrade_cost().amount}만원",
                    ["BUILD", "PASS"],
                    lambda choice: self.handle_upgrade_choice(choice, player, BuildingType.LANDMARK),
                    player=player,
                    property=self
                )
            elif level < 3:  # 아직 호텔이 없다면
                # 현재 레벨부터 랩 수에 맞는 옵션 제공
                options = []
                for building in available_buildings:
                    if (building == "별장" and level < 1) or \
                            (building == "빌딩" and level < 2) or \
                            (building == "호텔" and level < 3):
                        options.append(building)

                if not options:
                    return LandResult(
                        f"현재 {self.get_name()}에 더 높은 건물을 지을 수 없습니다.\n"
                        f"더 많은 바퀴를 돌아야 업그레이드가 가능합니다.",
                        ["OK"],
                        lambda _: None,
                        player=player,
                        property=self
                    )

                options.append("PASS")
                return LandResult(
                    f"{self.get_name()}에 어떤 건물을 건설하시겠습니까?",
                    options,
                    lambda choice: self.handle_building_selection(choice, player),
                    player=player,
                    property=self
                )
            elif level == 3 and not can_build_landmark:
                return LandResult(
                    f"{self.get_name()}에 랜드마크를 건설하려면 보드를 4바퀴 이상 돌아야 합니다.\n"
                    f"현재 {lap_count + 1}바퀴째 진행 중입니다.",
                    ["OK"],
                    lambda _: None,
                    player=player,
                    property=self
                )
            elif self._building.is_maxed():
                return LandResult(
                    f"{self._name}은 이미 랜드마크까지 건설된 상태입니다!",
                    ["OK"],
                    lambda _: None,
                    player=player,
                    property=self
                )
        else:
            # 다른 플레이어 소유지: 통행료 지불 및 인수 여부 묻기 (기존 코드와 동일)
            toll = self._building.calculate_toll(self._is_festival, self._attack_effect_value)

            def handle_toll_payment(choice: str):
                if player.get_cash().amount >= toll.amount:
                    player.spend(toll)
                    self._owner.receive(toll)
                    print(f"{player.get_name()}님이 {self.get_name()}의 통행료 {toll}를 지불했습니다.")

                    # 랜드마크가 건설되어있다면 통행료만 지불하고 인수는 할 수 없음
                    if self._building.get_level() == 4:
                        return LandResult(
                            f"{self.get_name()}에 랜드마크가 건설되어 있어 인수할 수 없습니다.",
                            ["OK"],
                            lambda _: None,
                            player=player,
                            property=self
                        )
                    else:
                        def handle_acquire(choice2: str):
                            if choice2 == "ACQUIRE":
                                self.purchase_from_owner(player)
                            else:
                                print("인수를 포기했습니다.")
                            return None

                        return LandResult(
                            f"{self.get_name()}을(를) 인수하시겠습니까?\n금액: {self._building.get_acquisition_cost().amount}만원",
                            ["ACQUIRE", "DECLINE"],
                            handle_acquire,
                            player=player,
                            property=self
                        )
                else:
                    print(f"{player.get_name()}님이 통행료를 낼 수 없습니다.")
                    return LandResult(
                        f"{player.get_name()}님의 잔액이 부족하여 통행료를 낼 수 없습니다.",
                        ["OK"],
                        lambda _: self._attempt_pay_with_sell(player, toll),
                        player=player,
                        property=self
                    )

            return LandResult(
                f"{self.get_name()}은(는) {self._owner.get_name()}의 소유입니다.\n통행료 {toll.amount}만원을 지불합니다.",
                ["OK"],
                handle_toll_payment,
                player=player,
                property=self
            )

    def handle_build_choice(self, choice: str, player: Player):
        lap_count = player.get_lap_count()

        if choice == "별장":
            cost = self._building.get_price()
            building_type = BuildingType.VILLA
            level = 1
        elif choice == "빌딩":
            if lap_count < 1:  # 2바퀴 이상 돌아야 빌딩 건설 가능
                return LandResult(
                    f"빌딩을 건설하려면 보드를 2바퀴 이상 돌아야 합니다.\n현재 {lap_count + 1}바퀴째 진행 중입니다.",
                    ["OK"],
                    lambda _: None,
                    player=player,
                    property=self
                )
            cost = self._building.get_price() * 1.5
            building_type = BuildingType.BUILDING
            level = 2
        elif choice == "호텔":
            if lap_count < 2:  # 3바퀴 이상 돌아야 호텔 건설 가능
                return LandResult(
                    f"호텔을 건설하려면 보드를 3바퀴 이상 돌아야 합니다.\n현재 {lap_count + 1}바퀴째 진행 중입니다.",
                    ["OK"],
                    lambda _: None,
                    player=player,
                    property=self
                )
            cost = self._building.get_price() * 2
            building_type = BuildingType.HOTEL
            level = 3
        elif choice == "PASS":
            return None
        else:
            return None

        # 이하 코드는 동일
        if player.get_cash().amount >= cost.amount:
            player.spend(cost)
            player.add_space(self)
            self._owner = player  # 땅 주인 설정
            self._building._level = level  # 건물 레벨 설정

            building_name = "별장"
            if building_type == BuildingType.BUILDING:
                building_name = "빌딩"
            elif building_type == BuildingType.HOTEL:
                building_name = "호텔"

            return LandResult(
                f"{self.get_name()}에 {building_name}을 건설했습니다!",
                ["OK"],
                lambda _: None,
                player=player,
                property=self
            )
        else:
            return LandResult(
                f"건설 비용이 부족합니다. 필요 비용: {cost.amount}만원",
                ["OK"],
                lambda _: None,
                player=player,
                property=self
            )

    def handle_building_selection(self, choice: str, player: Player):
        lap_count = player.get_lap_count()

        if choice == "별장":
            cost = self._building.get_price()
            building_type = BuildingType.VILLA
            level = 1
        elif choice == "빌딩":
            if lap_count < 1:  # 2바퀴 이상 돌아야 빌딩 건설 가능
                return LandResult(
                    f"빌딩을 건설하려면 보드를 2바퀴 이상 돌아야 합니다.\n현재 {lap_count + 1}바퀴째 진행 중입니다.",
                    ["OK"],
                    lambda _: None,
                    player=player,
                    property=self
                )
            cost = self._building.get_price() * 1.5
            building_type = BuildingType.BUILDING
            level = 2
        elif choice == "호텔":
            if lap_count < 2:  # 3바퀴 이상 돌아야 호텔 건설 가능
                return LandResult(
                    f"호텔을 건설하려면 보드를 3바퀴 이상 돌아야 합니다.\n현재 {lap_count + 1}바퀴째 진행 중입니다.",
                    ["OK"],
                    lambda _: None,
                    player=player,
                    property=self
                )
            cost = self._building.get_price() * 2
            building_type = BuildingType.HOTEL
            level = 3
        elif choice == "PASS":
            return None
        else:
            return None

        # 이하 코드는 동일
        if player.get_cash().amount >= cost.amount:
            player.spend(cost)
            player.add_space(self)
            self._building._level = level  # 건물 레벨 직접 설정

            building_name = "별장"
            if building_type == BuildingType.BUILDING:
                building_name = "빌딩"
            elif building_type == BuildingType.HOTEL:
                building_name = "호텔"

            return LandResult(
                f"{self.get_name()}에 {building_name}을 건설했습니다!",
                ["OK"],
                lambda _: None,
                player=player,
                property=self
            )
        else:
            return LandResult(
                f"건설 비용이 부족합니다. 필요 비용: {cost.amount}만원",
                ["OK"],
                lambda _: None,
                player=player,
                property=self
            )

    def handle_upgrade_choice(self, choice: str, player: Player, building_type: BuildingType):
        if choice == "BUILD":
            lap_count = player.get_lap_count()
            if lap_count < 3 and building_type == BuildingType.LANDMARK:
                return LandResult(
                    f"랜드마크를 건설하려면 보드를 4바퀴 이상 돌아야 합니다.\n"
                    f"현재 {lap_count + 1}바퀴째 진행 중입니다.",
                    ["OK"],
                    lambda _: None,
                    player=player,
                    property=self
                )

            cost = self._building.get_upgrade_cost()
            if player.get_cash().amount >= cost.amount:
                player.spend(cost)
                self._building.upgrade()  # 랜드마크로 업그레이드

                return LandResult(
                    f"{self.get_name()}에 랜드마크를 건설했습니다!",
                    ["OK"],
                    lambda _: None,
                    player=player,
                    property=self
                )
            else:
                return LandResult(
                    f"건설 비용이 부족합니다. 필요 비용: {cost.amount}만원",
                    ["OK"],
                    lambda _: None,
                    player=player,
                    property=self
                )
        return None

    def buy_land(self, player: Player):
        price = self._building.get_price()
        if player.get_cash().amount >= price.amount:
            player.spend(price)
            player.add_space(self)
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
            self._try_upgrade(player, cost, "랜드마크")
        elif self._building.is_maxed():
            print(f"{self._name}은 이미 랜드마크까지 건설된 상태입니다!")

    def _try_upgrade(self, player: Player, cost: Money, building_name: str):
        if player.get_cash().amount >= cost.amount:
            player.spend(cost)
            self._building.upgrade()
            print(f"{player}님이 {self._name}에 {building_name}을 건설했습니다!")
        else:
            print(f"{building_name} 건설 비용이 부족합니다.")

    def pay_toll(self, player: Player, seq: int = None):
        toll = self._building.calculate_toll(self._is_festival, self._attack_effect_value)
        if player.get_cash().amount >= toll.amount:
            player.spend(toll)
            self._owner.receive(toll)
            print(f"{player}님이 {self._name}의 통행료 {toll}를 지불했습니다!")
            if not seq:
                return LandResult(
                    f"{player}님이 {self._name}의 통행료 {toll}를 지불했습니다!",
                    ["OK"],
                    lambda _: None
                )
            else:
                return LandResult(
                    f"{player}님이 {self._name}의 통행료 {toll}를 지불했습니다!",
                    ["OK"],
                    lambda _: None,
                    on_complete_seq=seq
                )
        else:
            print(f"{player}님이 통행료를 지불할 금액이 부족합니다. (파산처리 등 추가 가능)")
            return self._attempt_pay_with_sell(player, toll)

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
            self._owner.remove_space(self)
            player.add_space(self)
            self._owner = player
            print(f"{player}님이 {self._name}을 인수했습니다!")
        else:
            print("인수 비용이 부족합니다.")
            return LandResult(
                "인수 비용이 부족합니다.",
                ["OK"],
                lambda _: None
            )

    def sale_land(self):
        price = self._building.get_price()
        self._owner.remove_space(self)
        self._owner = None
        self._building._level = 0
        print("매각")
        return price

    def _attempt_pay_with_sell(self, player: Player, toll: Money):
        sellable = player.get_spaces()
        sellable_msg = ""
        for idx, prop in enumerate(sellable):
            name = getattr(prop, "_name", f"도시{idx + 1}")
            sellable_msg += f"{idx}: {name}\n"

        if not sellable:
            # 파산 처리
            player.set_bankrupt()
            return LandResult(
                f"{player.get_name()}님은 통행료({toll.amount}원)를 낼 수 없어 파산했습니다.",
                ["OK"],
                lambda _: None
            )

        def handle_property_sell(input_text: str, sellable_list: list):
            seq = int(input_text.strip())
            message = ""
            target_city = None

            if seq < 0 or seq > len(sellable_list):
                message = f"잘못된 입력입니다.\n다른 도시 번호를 입력하세요"
            else:
                target_city = sellable_list[seq]
                if not (isinstance(target_city, PropertySpace) or isinstance(target_city, TouristSpotSpace)):
                    message = f"도시가 아닙니다.\n다른 도시 번호를 입력하세요"
            if target_city:
                gain = target_city.sale_land()
                player.get_cash().amount += gain.amount
                print(f"{target_city.get_name()}을 매각하고 {gain}을 확보했습니다.")
                return LandResult(
                    message=f"{target_city.get_name()}을 매각하고 {gain}을 확보했습니다.",
                    actions=["OK"],
                    callback=lambda _: self.pay_toll(player, target_city.get_seq()),
                )
            else:
                print("선택한 건물을 찾을 수 없습니다.")

            return self.pay_toll(player)

        return LandResult(
            message=f"현금이 부족합니다. 통행료 {toll.amount}원을 내기 위해 매각할 건물을 선택하세요\n" + sellable_msg,
            actions=["OK"],
            callback = lambda new_input: handle_property_sell(new_input, sellable),
            is_prompt = True
        )

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