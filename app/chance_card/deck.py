import random
from typing import List, Optional

from app.chance_card.abstract import ChanceCard

from app.chance_card.attack import *
#from app.chance_card.defence import *
from app.chance_card.event import *


class ChanceCardDeck:
    def __init__(self):
        self._deck = self.initial_cards()
        self._discard_deck = []
        random.shuffle(self._deck)

    def initial_cards(self) -> list[ChanceCard]:
        return [
            # AlienInvasionCard(),
             BlackoutCard(),
            # CityChangeCard(),
            # CityDonationCard(),
             EarthquakeCard(),
            # ForceTaxCard(),
             ForcedCitySaleCard(),
            # InfectiousDiseaseCard(),
             YellowDustCard(),
            # AngelCard(),
            # DiscountCouponCard(),
            # IslandEscapeCard(),
            # ShieldCard(),
            # TollFreeCard(),
             FestivalCard(),
             DesertIslandMoveCard(),
             StartMoveCard(),
             TaxPenaltyCard(),
             WorldTravelCard()
        ]

    def draw(self) -> Optional[ChanceCard]:
        if not self._deck:
            print("찬스 카드가 모두 소진되었습니다. 덱을 다시 섞습니다.")
            self.reset()
        return self._deck.pop() if self._deck else None

    def reset(self):
        self._deck = self._discard_deck[:]
        self._discard_deck = []
        random.shuffle(self._deck)

    def remaining_count(self) -> int:
        return len(self._deck)

    def discard(self, card: ChanceCard):
        self._discard_deck.append(card)