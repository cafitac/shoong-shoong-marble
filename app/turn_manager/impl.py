# 이 파일은 턴 관리를 담당하는 TurnManager 클래스를 구현합니다.
from app.player.impl import Player


class TurnManager:
    def __init__(self, players: list[Player]):
        self._players = players
        self._current_player_index = 0
        self._skipped_players = set()  # 스킵된 플레이어 목록

    def get_current_player(self) -> Player:
        """현재 턴의 플레이어를 반환합니다."""
        return self._players[self._current_player_index]

    def next(self) -> Player:
        """다음 플레이어로 턴을 넘깁니다."""
        # 현재 플레이어 인덱스 갱신
        self._current_player_index = (self._current_player_index + 1) % len(self._players)

        # 스킵해야 하는 플레이어인 경우 건너뛰기
        current_player = self.get_current_player()
        if current_player.is_turn_blocked():
            # 차단된 턴 감소
            current_player.next_turn()

            # 아직 턴이 차단되어 있다면 다음 플레이어로 한 번 더 넘기기
            if current_player.is_turn_blocked():
                print(f"{current_player.get_name()}의 턴이 스킵됩니다. 남은 차단 턴: {current_player._turns_to_wait}")
                return self.next()

        return self.get_current_player()

    def skip_player(self, player: Player, turns: int = 1) -> None:
        """
        특정 플레이어의 턴을 지정된 횟수만큼 스킵합니다.
        """
        player.turn_blocked(turns)
        self._skipped_players.add(player)
        print(f"{player.get_name()}의 턴이 {turns}회 스킵됩니다.")

    def is_player_skipped(self, player: Player) -> bool:
        """
        플레이어가 현재 스킵 상태인지 확인합니다.
        """
        return player in self._skipped_players and player.is_turn_blocked()

    def unskip_player(self, player: Player) -> None:
        """
        플레이어의 스킵 상태를 해제합니다.
        """
        if player in self._skipped_players:
            player.leave_island()  # 턴 차단 해제
            self._skipped_players.remove(player)
            print(f"{player.get_name()}의 턴 스킵이 해제되었습니다.")