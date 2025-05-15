from app.money.impl import Money


class Player:
    _wallet: Money

    def __init__(self) -> None:
        self._wallet = Money.zero()

    def get_assets(self) -> Money:
        return self._wallet

    def spend(self, amount: Money) -> None:
        self._wallet = self._wallet + amount
