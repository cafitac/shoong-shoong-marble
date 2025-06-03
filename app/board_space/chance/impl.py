from app.board_space.abstract import BoardSpace
from app.player.impl import Player


class ChanceSpace(BoardSpace):

    def on_land(self, player: Player):
        print(f"{player}님이 찬스 카드에 도착했습니다. 새 찬스 카드를 뽑습니다.")
        print("단, 찬스 카드는 1개만 보유할 수 있고 이미 카드를 보유한 경우 \"버리기\", \"즉시 사용\", \"교체\" 중 하나를 선택해야 합니다.")
        
        # TODO : 찬스 카드 구현 로직 구현 이후 로직을 추가합니다.

        pass
