from decimal import Decimal, ROUND_HALF_UP


class Money:
    def __init__(self, amount):
        amount = Decimal(str(amount)).quantize(Decimal("1."), rounding=ROUND_HALF_UP)
        if amount < 0:
            raise ValueError("금액은 음수일 수 없습니다.")
        self.amount = amount

    def __str__(self):
        return f"{self.amount:,}원"

    def __repr__(self):
        return f"{self.__class__.__name__}(amount={self.amount:,})"

    def __add__(self, other):
        return Money(self.amount + other.amount)

    def __sub__(self, other):
        if self.amount - other.amount < 0:
            raise ValueError("잔액이 부족합니다.")

        return Money(self.amount - other.amount)

    def __mul__(self, multiplier):
        return Money(self.amount * Decimal(str(multiplier)))

    def __truediv__(self, divisor):
        return Money(self.amount / Decimal(str(divisor)))

    def __eq__(self, other):
        return self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __le__(self, other):
        return self.amount <= other.amount

    def __gt__(self, other):
        return self.amount > other.amount

    def __ge__(self, other):
        return self.amount >= other.amount

    @classmethod
    def zero(cls) -> "Money":
        return cls(0)
