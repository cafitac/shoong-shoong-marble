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
                    return self._attempt_pay_with_sell(player, toll)

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
            player.add_space(self)
            print(f"{player}님이 {self._name}을 구매했습니다!")
        else:
            print(f"{player}님은 돈이 부족하여 {self._name}을 구매할 수 없습니다.")

    def sale_land(self):
        price = self._base_price
        self._owner.remove_space(self)
        self._owner = None
        print("매각")
        return price

    def pay_toll(self, player: Player, sell_spaces = None):
        toll = self._base_price
        if player.get_cash().amount >= toll.amount:
            player.spend(toll)
            self._owner.receive(toll)
            print(f"{player}님이 {self._name}의 통행료 {toll}를 지불했습니다!")
            if not sell_spaces:
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
                    on_complete_seq=sell_spaces
                )
        else:
            print(f"{player}님이 통행료를 지불할 금액이 부족합니다. (파산처리 등 추가 가능)")
            return self._attempt_pay_with_sell(player, toll, sell_spaces)

    def _attempt_pay_with_sell(self, player: Player, toll: Money, sell_spaces = None):
        if sell_spaces is None:
            sell_spaces = list()
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
                lambda _: None,
                on_complete_seq=sell_spaces
            )

        def handle_property_sell(input_text: str, sellable_list: list):
            seq = int(input_text.strip())
            message = ""
            target_city = None

            if seq < 0 or seq > len(sellable_list):
                message = f"잘못된 입력입니다.\n다른 도시 번호를 입력하세요"
            else:
                target_city = sellable_list[seq]

            if target_city:
                sell_spaces.append(target_city.get_seq())
                gain = target_city.sale_land()
                player.get_cash().amount += gain.amount
                print(f"{target_city.get_name()}을 매각하고 {gain}을 확보했습니다.")
                return LandResult(
                    message=f"{target_city.get_name()}을 매각하고 {gain}을 확보했습니다.",
                    actions=["OK"],
                    callback=lambda _: self.pay_toll(player, sell_spaces),
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

    def get_owner(self) -> Player:
        return self._owner