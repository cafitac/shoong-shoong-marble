# 이 파일은 플레이어 위치 관리를 담당하는 PositionManager 클래스를 구현합니다.
from app.board.impl import Board
from app.board_space.abstract import BoardSpace
from app.player.impl import Player


class PositionManager:
    def __init__(self, board: Board, players: list[Player]):
        self._board = board
        self._players = players
        self._positions = {player: 0 for player in players}  # 각 플레이어의 위치 인덱스

        # 각 위치(인덱스)에 있는 플레이어 목록
        self._players_at_position = {}
        self._init_players_at_position()

        # 디버깅을 위한 로그 출력
        print("초기 플레이어 위치:")
        for player in players:
            print(f"{player.get_name()} (ID: {player.get_idx()}): 위치 {self._positions[player]}")

    def _init_players_at_position(self):
        """
        모든 플레이어를 시작 위치에 배치합니다.
        """
        for player in self._players:
            position = self._positions[player]
            if position not in self._players_at_position:
                self._players_at_position[position] = []
            self._players_at_position[position].append(player)

    def get_position(self, player: Player) -> int:
        """
        플레이어의 현재 위치 인덱스를 반환합니다.
        """
        return self._positions.get(player, 0)

    def get_location(self, player: Player) -> BoardSpace:
        """
        플레이어가 위치한 보드 칸을 반환합니다.
        """
        position = self._positions.get(player, 0)
        return self._board.get_space(position)  # get_space_at 대신 get_space 사용

    def _get_board_size(self) -> int:
        """
        보드의 크기(칸 수)를 반환합니다.
        """
        spaces = getattr(self._board, "_spaces", [])
        return len(spaces)

    def move(self, player: Player, steps: int) -> BoardSpace:
        """
        플레이어를 지정된 칸 수만큼 이동시키고, 도착한 보드 칸을 반환합니다.
        """
        # 디버깅 정보
        print(f"\n이동 시작: {player.get_name()} (ID: {player.get_idx()})")
        print(f"현재 위치: {self._positions[player]}, 이동할 칸 수: {steps}")

        # 현재 위치에서 플레이어 제거
        old_position = self._positions[player]
        if old_position in self._players_at_position and player in self._players_at_position[old_position]:
            self._players_at_position[old_position].remove(player)

        # 새 위치 계산 (보드 크기를 초과하면 한 바퀴 돌아서 계산)
        board_size = self._get_board_size()
        print(f"보드 크기: {board_size}")
        new_position = (old_position + steps) % board_size
        self._positions[player] = new_position

        print(f"새 위치: {new_position}")

        # 새 위치에 플레이어 추가
        if new_position not in self._players_at_position:
            self._players_at_position[new_position] = []
        self._players_at_position[new_position].append(player)

        # 한 바퀴 돌았는지 확인 (시작점을 지나갔는지)
        if new_position < old_position or (old_position + steps) >= board_size:
            # 시작점을 지나갔을 때 30만원 지급
            from app.money.impl import Money
            reward = Money(300000)
            player.receive(reward)
            print(f"{player.get_name()}이(가) 출발점을 통과하여 {reward}을(를) 받았습니다!")

        # 모든 플레이어의 현재 위치 출력 (디버깅용)
        print("\n현재 모든 플레이어의 위치:")
        for p in self._players:
            print(f"{p.get_name()} (ID: {p.get_idx()}): 위치 {self._positions[p]}")

        return self._board.get_space(new_position)  # get_space_at 대신 get_space 사용

    def set_position(self, player: Player, position: int) -> BoardSpace:
        """
        플레이어를 지정된 위치로 직접 이동시킵니다.
        (특정 이벤트나 카드 효과 등에 사용)
        """
        # 디버깅 정보
        print(f"\n위치 설정: {player.get_name()} (ID: {player.get_idx()})")
        print(f"이전 위치: {self._positions.get(player, 0)}, 설정할 위치: {position}")

        # 현재 위치에서 플레이어 제거
        old_position = self._positions.get(player, 0)
        if old_position in self._players_at_position and player in self._players_at_position[old_position]:
            self._players_at_position[old_position].remove(player)

        # 위치 범위 확인
        board_size = self._get_board_size()
        if position < 0 or position >= board_size:
            position = position % board_size
            print(f"위치 범위 조정: {position}")

        # 새 위치 설정
        self._positions[player] = position

        # 새 위치에 플레이어 추가
        if position not in self._players_at_position:
            self._players_at_position[position] = []
        self._players_at_position[position].append(player)

        # 모든 플레이어의 현재 위치 출력 (디버깅용)
        print("\n현재 모든 플레이어의 위치:")
        for p in self._players:
            print(f"{p.get_name()} (ID: {p.get_idx()}): 위치 {self._positions[p]}")

        return self._board.get_space(position)  # get_space_at 대신 get_space 사용

    def get_players_at_position(self, position: int) -> list[Player]:
        """
        특정 위치에 있는 모든 플레이어 목록을 반환합니다.
        """
        return self._players_at_position.get(position, [])

    def move_all_players(self, position: int) -> None:
        """
        모든 플레이어를 특정 위치로 이동시킵니다.
        (특정 이벤트나 게임 초기화 등에 사용)
        """
        print(f"\n모든 플레이어를 위치 {position}으로 이동합니다.")
        for player in self._players:
            self.set_position(player, position)

    def update_player_position(self, player: Player, position: int) -> None:
        """
        UI 렌더링용 플레이어 위치 업데이트 함수
        """
        self.set_position(player, position)