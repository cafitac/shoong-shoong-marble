from app.player.impl import Player


class TurnManager:
    _players: list[Player] = []
    _current_player: Player

    def __init__(self, players: list[Player]):
        self._players = players
        self._current_player = players[0]

    def get_current_player(self) -> Player:
        return self._current_player

    def next(self) -> Player:
        self._current_player = self._players[(self._players.index(self._current_player) + 1) % len(self._players)]

        # 현재 플레이어가 현재 턴을 수행할 수 있는 상태가 아니라면 다음 플레이어로 스킵
        if self._current_player.is_turn_blocked():
            self._current_player.next_turn()
            return self.next()

        return self._current_player
