from app.board_space.abstract import BoardSpace
from app.board_space.land_result import LandResult
from app.chance_card.abstract import ChanceCardType
from app.chance_card.deck import ChanceCardDeck
from app.player.impl import Player
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game


class ChanceSpace(BoardSpace):
    def __init__(self, seq: int, name: str):
        super().__init__(seq, name)
        self.game = None

    def on_land(self, player: Player):
        card = self.game.get_card_deck().draw()

        #print(f"{player}님이 찬스 카드에 도착했습니다. 새 찬스 카드를 뽑습니다.")
        #print("단, 찬스 카드는 1개만 보유할 수 있고 이미 카드를 보유한 경우 \"버리기\", \"즉시 사용\", \"교체\" 중 하나를 선택해야 합니다.")
        card_msg = f"{player.get_name()}님이 찬스 카드에 도착했습니다.\n" \
                   f"새 찬스 카드를 뽑습니다: {card.name} ({card.description})"

        if card.card_type == ChanceCardType.INSTANT: # 즉시 사용
            self.game.get_card_deck().discard(card)
            return LandResult(
                card_msg + "\n이 카드는 즉시 발동됩니다.",
                ["OK"],
                lambda _: card.use(self.game)
            )
        elif card.card_type == ChanceCardType.KEEP: # 보관 가능
            if player.get_card() is not None: # 갖고 있는 카드가 있을 경우 교체/버리기
                def handle_choice(choice: str):
                    if choice == "DISCARD":
                        self.game.get_card_deck().discard(card)
                    elif choice == "REPLACE":
                        self.game.get_card_deck().discard(player.get_card())
                        player.set_card(card)

                return LandResult(
                    card_msg + "\n이미 카드를 보유 중입니다. 선택하세요.",
                    ["DISCARD", "REPLACE"],
                    handle_choice
                )
            else: # 갖고 있는 카드가 없을 경우 보관
                player.set_card(card)
                return LandResult(
                    card_msg + "\n자동으로 보관합니다.",
                    ["OK"],
                    lambda _: None
                )
        return None

    def set_deck(self, game: 'Game'):
        self.game = game
