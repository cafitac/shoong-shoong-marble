from app.player.impl import Player
import random

class TurnManager:
    _players: list[Player] = []
    _current_player: Player

    def __init__(self, players: list[Player]):
        self._players = players
        self._current_player = players[0]

    def get_current_player(self) -> Player:
        return self._current_player
    
    def roll_dice() -> int:
        return random.randint(1, 6)

    def next(self) -> Player:
        self._current_player = self._players[(self._players.index(self._current_player) + 1) % len(self._players)]

        # 현재 플레이어가 섬에 있는 경우 주사위가 더블이 나오면 즉시 탈출합니다.
        if self._current_player.is_on_island():
            print(f"{self._current_player}님은 무인도에 있습니다. 주사위를 굴려주세요.")

            # TODO : 실제 주사위 굴리기 버튼을 통해 주사위를 굴리는 로직으로 변경이 필요합니다.
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)

            print(f"주사위 결과: {dice1}, {dice2}")
            if dice1 == dice2:
                print("더블! 무인도에서 탈출합니다.")
                self._current_player.leave_island()
            else:
                self._current_player.next_turn()  # 한 턴 차감
                print(f"{self._current_player}님은 아직 {self._current_player._turns_to_wait}턴 남았습니다.")
                if self._current_player._turns_to_wait <= 0:
                    self._current_player.leave_island()
            return self._current_player

        # 현재 플레이어가 현재 턴을 수행할 수 있는 상태가 아니라면 다음 플레이어로 스킵
        if self._current_player.is_turn_blocked():
            self._current_player.next_turn()
            return self.next()
        
        return self._current_player
