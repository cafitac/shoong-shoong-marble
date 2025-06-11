import math
from typing import List, Tuple

import pygame

from app.board_space.abstract import BoardSpace
from app.player.impl import Player
from ui.board_block import BoardBlock
from ui.constants import BOARD_CONTENT_HEIGHT, BOARD_CONTENT_WIDTH, BOARD_EDGES, CELL_LONG, CELL_SHORT, COLOR_BLACK, \
    COLOR_CORNER_FILL, COLOR_WHITE, \
    CORNER_POSITIONS, CORNER_SIDE
from ui.corner_block import CornerBlock


class BoardRenderer:
    def __init__(self, board_surface, fonts, colors, board_spaces: List[BoardSpace], position_manager=None):
        self.board_surface = board_surface
        self.fonts = fonts
        self.colors = colors
        self.rotation_angle = 45
        self.board_spaces = board_spaces  # 모든 공간 (코너 + 일반)
        self.position_manager = position_manager
        self.player_token_radius = 15  # 플레이어 토큰 반지름
        self._init_blocks()
        self._draw_initial_board()

    def _init_blocks(self):
        # 각 코너 위치의 seq 매핑
        corner_spaces = []
        spaces_by_seq = {space.get_seq(): space for space in self.board_spaces}

        # 코너 위치 매핑 정의 (시작 -> 무인도 -> 축제 -> 슝슝여행 순서로)
        corner_seq_map = {0: 0, 24: 1, 8: 2, 16: 3}  # seq:CORNER_POSITIONS 인덱스

        # 코너 블록 공간 찾기
        for seq in corner_seq_map.keys():
            if seq in spaces_by_seq:
                corner_spaces.append(spaces_by_seq[seq])

        # 코너 블록 생성
        self.corner_blocks = [
            CornerBlock(
                CORNER_SIDE, COLOR_CORNER_FILL, COLOR_BLACK, space, font=self.fonts['corner']
            ) for space in corner_spaces
        ]

        # 코너가 아닌 일반 블록 공간 찾기
        corner_seqs = set(corner_seq_map.keys())
        non_corner_spaces = [space for space in self.board_spaces if space.get_seq() not in corner_seqs]

        # BoardBlock 객체로 변환
        all_non_corner_blocks = [
            BoardBlock(
                CELL_SHORT, CELL_LONG, space, self.colors,
                {'main': self.fonts['main'], 'price': self.fonts['price']}
            ) for space in non_corner_spaces
        ]

        # 각 라인별로 사용할 BoardBlock 객체들을 미리 준비 (seq 기준으로 필터링 및 정렬)
        self.left_line_blocks = sorted(
            [block for block in all_non_corner_blocks if 1 <= block.space.get_seq() <= 7],
            key=lambda b: b.space.get_seq()
        )
        self.top_line_blocks = sorted(
            [block for block in all_non_corner_blocks if 9 <= block.space.get_seq() <= 15],
            key=lambda b: b.space.get_seq()
        )
        self.right_line_blocks = sorted(
            [block for block in all_non_corner_blocks if 17 <= block.space.get_seq() <= 23],
            key=lambda b: b.space.get_seq()
        )
        self.bottom_line_blocks = sorted(
            [block for block in all_non_corner_blocks if 25 <= block.space.get_seq() <= 31],
            key=lambda b: b.space.get_seq()
        )

    def _draw_initial_board(self):
        for corner_block, (cx, cy) in zip(self.corner_blocks, CORNER_POSITIONS):
            corner_block.draw(self.board_surface, cx, cy)
        self._draw_all_lines()

    def _draw_all_lines(self):
        # 왼쪽 라인 (seq 1-7, 아래 -> 위)
        center_x_left = BOARD_EDGES['left'] + CELL_LONG / 2
        current_y_left = BOARD_EDGES['bottom'] - CORNER_SIDE
        for block in self.left_line_blocks:  # seq 1, 2, ..., 7 순서
            center_y_block = current_y_left - CELL_SHORT / 2
            block.draw(self.board_surface, center_x_left, center_y_block, 90)
            current_y_left -= CELL_SHORT

        # 위쪽 라인 (seq 9-15, 좌 -> 우)
        center_y_top = BOARD_EDGES['top'] + CELL_LONG / 2
        current_x_top = BOARD_EDGES['left'] + CORNER_SIDE
        for block in self.top_line_blocks:  # seq 9, 10, ..., 15 순서
            center_x_block = current_x_top + CELL_SHORT / 2
            block.draw(self.board_surface, center_x_block, center_y_top, 0)
            current_x_top += CELL_SHORT

        # 오른쪽 라인 (seq 17-23, 위 -> 아래)
        center_x_right = BOARD_EDGES['right'] - CELL_LONG / 2
        current_y_right = BOARD_EDGES['top'] + CORNER_SIDE
        for block in self.right_line_blocks:  # seq 17, 18, ..., 23 순서
            center_y_block = current_y_right + CELL_SHORT / 2
            block.draw(self.board_surface, center_x_right, center_y_block, 90)
            current_y_right += CELL_SHORT

        # 아래쪽 라인 (seq 25-31, 우 -> 좌)
        center_y_bottom = BOARD_EDGES['bottom'] - CELL_LONG / 2
        current_x_bottom = BOARD_EDGES['right'] - CORNER_SIDE
        # seq 25, 26, ..., 31 순서대로 가져왔으므로, 그릴 때 x 좌표를 우측부터 시작하여 좌측으로 이동
        for block in self.bottom_line_blocks:
            center_x_block = current_x_bottom - CELL_SHORT / 2
            block.draw(self.board_surface, center_x_block, center_y_bottom, 0)
            current_x_bottom -= CELL_SHORT

    def draw_board(self, screen, center_x, center_y):
        current_w, current_h = screen.get_size()
        scale_factor = self._calculate_scale_factor(current_w, current_h)

        # 플레이어 말을 그리기 위한 임시 보드 생성
        temp_board = pygame.Surface((BOARD_CONTENT_WIDTH, BOARD_CONTENT_HEIGHT), pygame.SRCALPHA)
        temp_board.blit(self.board_surface, (0, 0))

        # 플레이어 말 그리기 (원본 크기 보드에)
        if self.position_manager:
            self._draw_player_tokens(temp_board)

        # 스케일링 및 회전
        scaled_board = self._scale_board(temp_board, scale_factor)
        rotated_board = pygame.transform.rotate(scaled_board, self.rotation_angle)
        rect = rotated_board.get_rect(center=(center_x, center_y))
        screen.blit(rotated_board, rect)

    def _draw_player_tokens(self, board_surface):
        # 각 위치별 플레이어 목록 생성
        players_at_position = {}
        for player in self.position_manager._players:
            if player._is_bankrupt:
                continue
            position = self.position_manager.get_position(player)
            if position not in players_at_position:
                players_at_position[position] = []
            players_at_position[position].append(player)

        # 각 위치에 플레이어 말 그리기
        for position, players in players_at_position.items():
            x, y = self._get_position_coordinates(position)
            self._draw_players_at_position(board_surface, x, y, players)

    def _draw_players_at_position(self, surface, x, y, players):
        """특정 위치에 있는 플레이어들을 그립니다."""
        num_players = len(players)
        radius = self.player_token_radius

        # 플레이어 수에 따른 배치 패턴
        offsets = [
            [],  # 0명
            [(0, 0)],  # 1명 (중앙)
            [(-radius * 1.2, 0), (radius * 1.2, 0)],  # 2명 (가로)
            [(-radius * 1.2, -radius * 1.2), (radius * 1.2, -radius * 1.2), (0, radius * 1.2)],  # 3명 (삼각형)
            [(-radius * 1.2, -radius * 1.2), (radius * 1.2, -radius * 1.2), (-radius * 1.2, radius * 1.2),
             (radius * 1.2, radius * 1.2)]  # 4명 (사각형)
        ]

        pattern = offsets[min(num_players, 4)]

        # 각 플레이어 말 그리기
        for i, player in enumerate(players[:4]):  # 최대 4명까지만 표시
            color = player.get_color()

            # 플레이어 위치 계산
            player_x = int(x + pattern[i][0])
            player_y = int(y + pattern[i][1])

            # 플레이어 말 그리기
            pygame.draw.circle(surface, color, (player_x, player_y), radius)
            pygame.draw.circle(surface, COLOR_BLACK, (player_x, player_y), radius, 2)  # 테두리

            # 플레이어 ID 표시
            player_id_str = str(player.get_idx() + 1)  # 1부터 시작하는 번호
            font = pygame.font.SysFont("Arial", max(10, 14), bold=True)
            text = font.render(player_id_str, True, COLOR_WHITE)
            text_rect = text.get_rect(center=(player_x, player_y))
            surface.blit(text, text_rect)

    def _get_position_coordinates(self, position: int) -> Tuple[float, float]:
        """주어진 위치(seq)에 해당하는 보드 상의 좌표를 계산합니다."""
        seq = position
        # 시작 -> 무인도 -> 축제 -> 슝슝여행 순서로 매핑
        corner_seq_map = {0: 0, 24: 1, 8: 2, 16: 3}  # seq:CORNER_POSITIONS 인덱스

        # 코너 블록인 경우
        if seq in corner_seq_map:
            return CORNER_POSITIONS[corner_seq_map[seq]]

        # 일반 블록인 경우
        # 왼쪽 라인 (seq 1-7, 아래 -> 위)
        if 1 <= seq <= 7:
            center_x = BOARD_EDGES['left'] + CELL_LONG / 2
            center_y = BOARD_EDGES['bottom'] - CORNER_SIDE - (seq - 0.5) * CELL_SHORT
            return center_x, center_y

        # 위쪽 라인 (seq 9-15, 좌 -> 우)
        elif 9 <= seq <= 15:
            center_x = BOARD_EDGES['left'] + CORNER_SIDE + (seq - 8.5) * CELL_SHORT
            center_y = BOARD_EDGES['top'] + CELL_LONG / 2
            return center_x, center_y

        # 오른쪽 라인 (seq 17-23, 위 -> 아래)
        elif 17 <= seq <= 23:
            center_x = BOARD_EDGES['right'] - CELL_LONG / 2
            center_y = BOARD_EDGES['top'] + CORNER_SIDE + (seq - 16.5) * CELL_SHORT
            return center_x, center_y

        # 아래쪽 라인 (seq 25-31, 우 -> 좌)
        elif 25 <= seq <= 31:
            center_x = BOARD_EDGES['right'] - CORNER_SIDE - (seq - 24.5) * CELL_SHORT
            center_y = BOARD_EDGES['bottom'] - CELL_LONG / 2
            return center_x, center_y

        # 정의되지 않은 위치
        print(f"경고: 플레이어 위치 seq {seq}는 정의된 보드 공간 범위를 벗어납니다.")
        return BOARD_EDGES['left'] + CORNER_SIDE / 2, BOARD_EDGES['bottom'] - CORNER_SIDE / 2

    def _rotate_point(self, x, y, angle_degrees):
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        return new_x, new_y

    def update_player_position(self, player: Player, position: int):
        if self.position_manager:
            self.position_manager.update_player_position(player, position)

    def _calculate_scale_factor(self, screen_width, screen_height):
        screen_diagonal = min(screen_width, screen_height) * 0.95
        original_diagonal = math.sqrt(BOARD_CONTENT_WIDTH ** 2 + BOARD_CONTENT_HEIGHT ** 2)
        scale_factor = screen_diagonal / original_diagonal
        max_scale = min(screen_width / BOARD_CONTENT_WIDTH,
                        screen_height / BOARD_CONTENT_HEIGHT) * 1.5
        return min(scale_factor, max_scale)

    def _scale_board(self, board_surface, scale_factor):
        scaled_width = max(10, int(board_surface.get_width() * scale_factor))
        scaled_height = max(10, int(board_surface.get_height() * scale_factor))
        return pygame.transform.smoothscale(board_surface, (scaled_width, scaled_height))

    def update_block_by_seq(self, seq: int):
        center_x, center_y, angle = 0, 0, 0
        if 1 <= seq <= 7:
            index = seq - 1
            block = self.left_line_blocks[index]
            center_x = BOARD_EDGES['left'] + CELL_LONG / 2
            center_y = BOARD_EDGES['bottom'] - CORNER_SIDE - (CELL_SHORT * index) - CELL_SHORT / 2
            angle = 90
        elif 9 <= seq <= 15:
            index = seq - 9
            block = self.top_line_blocks[index]
            center_x = BOARD_EDGES['left'] + CORNER_SIDE + (CELL_SHORT * index) + CELL_SHORT / 2
            center_y = BOARD_EDGES['top'] + CELL_LONG / 2
            angle = 0
        elif 17 <= seq <= 23:
            index = seq - 17
            block = self.right_line_blocks[index]
            center_x = BOARD_EDGES['right'] - CELL_LONG / 2
            center_y = BOARD_EDGES['top'] + CORNER_SIDE + (CELL_SHORT * index) + CELL_SHORT / 2
            angle = 90
        elif 25 <= seq <= 31:
            index = seq - 25
            block = self.bottom_line_blocks[index]
            center_x = BOARD_EDGES['right'] - CORNER_SIDE - (CELL_SHORT * index) - CELL_SHORT / 2
            center_y = BOARD_EDGES['bottom'] - CELL_LONG / 2
            angle = 0
        else:
            return

        block.update_text()
        block.draw(self.board_surface, center_x, center_y, angle)