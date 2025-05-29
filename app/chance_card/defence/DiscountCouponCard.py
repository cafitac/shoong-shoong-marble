from app.chance_card.abstract import ChanceCard

# 할인 쿠폰
# 다음 통행료 50 % 할인 1회
class DiscountCouponCard(ChanceCard):
    def __init__(self):
        self.name = "할인 쿠폰"
        self.description = "통행료 50 % 할인 1회"

    def use(self):
        # 통행료 50% 할인
        return True
