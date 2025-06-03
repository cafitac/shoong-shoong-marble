import math
import pygame
from typing import Dict, List
from app.player.impl import Player
from app.board_space.abstract import BoardSpace
from ui.board_block import BoardBlock
from ui.corner_block import CornerBlock
from ui.constants import (
    BOARD_CELLS_PER_SIDE,  # 각 변의 일반 셀 개수, 7로 가정
    CELL_LONG,
    CELL_SHORT,
    CORNER_SIDE,
    BOARD_EDGES,
    CORNER_POSITIONS,
    BOARD_CONTENT_WIDTH,
    BOARD_CONTENT_HEIGHT,
    COLOR_CORNER_FILL,
    COLOR_BLACK
)


class BoardRenderer:
    def __init__(self, board_surface, fonts, colors, board_spaces: List[BoardSpace], position_manager=None):
        self.board_surface = board_surface
        self.fonts = fonts
        self.colors = colors
        self.rotation_angle = 45
        self.board_spaces = board_spaces  # 모든 공간 (코너 + 일반)
        self.position_manager = position_manager
        self._init_blocks()
        self._draw_initial_board()

    def _init_blocks(self):
        corner_seq_map = {
            "START": 0,
            "ISLAND": 8,
            "FESTIVAL": 16,
            "TRAVEL": 24,
        }
        spaces_by_seq = {space.get_seq(): space for space in self.board_spaces}

        _corner_space_objects = [
            spaces_by_seq.get(corner_seq_map["START"]),
            spaces_by_seq.get(corner_seq_map["TRAVEL"]),
            spaces_by_seq.get(corner_seq_map["ISLAND"]),
            spaces_by_seq.get(corner_seq_map["FESTIVAL"]),
        ]

        corner_spaces_for_blocks = [cs for cs in _corner_space_objects if cs is not None]

        self.corner_blocks = [
            CornerBlock(
                CORNER_SIDE, COLOR_CORNER_FILL, COLOR_BLACK, space, font=self.fonts['corner']
            ) for space in corner_spaces_for_blocks
        ]

        corner_seqs = set(corner_seq_map.values())
        non_corner_space_objects = [
            space for space in self.board_spaces if space.get_seq() not in corner_seqs
        ]
        # BoardBlock 객체로 변환
        all_non_corner_blocks = [
            BoardBlock(
                CELL_SHORT, CELL_LONG, space, self.colors,
                {'main': self.fonts['main'], 'price': self.fonts['price']}
            ) for space in non_corner_space_objects
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
        scaled_board = self._scale_board(scale_factor)
        rotated_board = pygame.transform.rotate(scaled_board, self.rotation_angle)
        rect = rotated_board.get_rect(center=(center_x, center_y))
        screen.blit(rotated_board, rect)
        if self.position_manager:
            self._draw_players(screen, rect, scale_factor)

    def _draw_players(self, screen, board_rect, scale_factor):
        # 참고: 이 함수는 플레이어 위치 계산 로직이 변경된 보드 레이아웃을 반영하도록 수정되어야 할 수 있습니다.
        for player in self.position_manager._positions.keys():
            position = self.position_manager._positions[player]  # 이 position이 새로운 보드 순서에 맞는 값인지 확인 필요
            pos_coords = self._get_position_coordinates(position, scale_factor)
            if pos_coords:
                x, y = pos_coords
                rotated_x, rotated_y = self._rotate_point(
                    x - board_rect.width / 2,
                    y - board_rect.height / 2,
                    self.rotation_angle
                )
                final_x = rotated_x + board_rect.centerx
                final_y = rotated_y + board_rect.centery
                player_radius = int(CELL_SHORT * scale_factor * 0.15)
                pygame.draw.circle(screen, player.get_color(), (int(final_x), int(final_y)), player_radius)

    def _get_position_coordinates(self, position: int, scale_factor: float) -> tuple[float, float]:
        # 경고: 이 함수는 변경된 보드 레이아웃(그리기 순서)을 반영하도록 수정되어야 합니다.
        # 현재는 플레이어 위치가 이전 보드 레이아웃 기준으로 계산될 수 있습니다.
        # 예를 들어, position이 BoardSpace의 seq 값과 동일하다면,
        # seq 1은 왼쪽 라인 하단, seq 9는 위쪽 라인 좌측 등의 위치로 계산되어야 합니다.
        # 이 함수의 수정은 PositionManager가 position 값을 어떻게 관리하는지에 따라 달라집니다.

        # 임시로 기존 로직 유지 (플레이어 위치가 올바르지 않을 수 있음)
        total_cell_count_per_side = 7  # BOARD_CELLS_PER_SIDE 와 동일해야 함

        # 코너를 포함한 전체 위치로 변환하는 로직 필요 (예: START=0, seq 1~7, ISLAND=8, seq 9~15 ...)
        # 아래는 매우 단순화된 예시이며, 실제 position 값의 의미에 따라 전면적인 재설계가 필요합니다.
        # 이 부분은 플레이어 이동 및 위치 관리 로직과 긴밀하게 연관되어 수정되어야 합니다.

        # --- 임시 플레이어 위치 계산 시작 (정확하지 않을 수 있음) ---
        # 이 코드는 실제 게임 로직과 맞지 않을 가능성이 매우 높으며, 개념적 예시입니다.
        # 올바른 플레이어 표시를 위해서는 PositionManager와 이 함수의 로직을 함께 검토해야 합니다.
        # 예를 들어, position이 csv의 seq와 동일하다고 가정.
        seq = position
        x, y = 0, 0

        # 해당 seq의 BoardBlock을 찾아서 그 Block의 space.get_seq()와 비교해야합니다.
        # 하지만 BoardBlock 자체는 BoardRenderer에 라인별로 저장되어 있어 직접 접근이 어렵습니다.
        # 따라서, 이 함수는 position (seq) 값을 받아서, 해당 seq가 어느 라인의 몇 번째 블록에 해당하는지
        # 그리고 그 블록의 중심 좌표가 어디인지를 계산해야 합니다.

        # 코너 블록의 seq와 일치하는지 확인
        corner_block_found = False
        for idx, cb in enumerate(self.corner_blocks):
            if cb.space.get_seq() == seq:  # CornerBlock도 space 속성을 가짐 (수정 필요 가정)
                # CornerBlock의 get_space()가 없다면, CornerBlock 생성자에 space를 저장하고 직접 접근해야 함
                # 여기서는 CornerBlock이 space 속성을 가지고 있고, 그 space가 get_seq()를 가진다고 가정
                x, y = CORNER_POSITIONS[idx]
                corner_block_found = True
                break

        if not corner_block_found:
            # 왼쪽 라인 (seq 1-7, 아래 -> 위)
            if 1 <= seq <= 7:
                block_index_in_line = seq - 1
                if 0 <= block_index_in_line < len(self.left_line_blocks):
                    center_x_left = BOARD_EDGES['left'] + CELL_LONG / 2
                    # 아래에서 위로 그리므로, 첫 블록(seq 1)이 가장 아래에 위치
                    base_y = BOARD_EDGES['bottom'] - CORNER_SIDE - CELL_SHORT / 2
                    y = base_y - block_index_in_line * CELL_SHORT
                    x = center_x_left
                else:
                    corner_block_found = True  # 임시로 에러 처리 대신 코너로 넘김
            # 위쪽 라인 (seq 9-15, 좌 -> 우)
            elif 9 <= seq <= 15:
                block_index_in_line = seq - 9
                if 0 <= block_index_in_line < len(self.top_line_blocks):
                    center_y_top = BOARD_EDGES['top'] + CELL_LONG / 2
                    # 좌에서 우로 그리므로, 첫 블록(seq 9)이 가장 왼쪽에 위치
                    base_x = BOARD_EDGES['left'] + CORNER_SIDE + CELL_SHORT / 2
                    x = base_x + block_index_in_line * CELL_SHORT
                    y = center_y_top
                else:
                    corner_block_found = True  # 임시
            # 오른쪽 라인 (seq 17-23, 위 -> 아래)
            elif 17 <= seq <= 23:
                block_index_in_line = seq - 17
                if 0 <= block_index_in_line < len(self.right_line_blocks):
                    center_x_right = BOARD_EDGES['right'] - CELL_LONG / 2
                    # 위에서 아래로 그리므로, 첫 블록(seq 17)이 가장 위에 위치
                    base_y = BOARD_EDGES['top'] + CORNER_SIDE + CELL_SHORT / 2
                    y = base_y + block_index_in_line * CELL_SHORT
                    x = center_x_right
                else:
                    corner_block_found = True  # 임시
            # 아래쪽 라인 (seq 25-31, 우 -> 좌)
            elif 25 <= seq <= 31:
                block_index_in_line = seq - 25
                if 0 <= block_index_in_line < len(self.bottom_line_blocks):
                    center_y_bottom = BOARD_EDGES['bottom'] - CELL_LONG / 2
                    # 우에서 좌로 그리므로, 첫 블록(seq 25)이 가장 오른쪽에 위치
                    base_x = BOARD_EDGES['right'] - CORNER_SIDE - CELL_SHORT / 2
                    x = base_x - block_index_in_line * CELL_SHORT
                    y = center_y_bottom
                else:
                    corner_block_found = True  # 임시
            else:
                print(f"Warning: Player position seq {seq} is out of defined board space ranges for non-corners.")
                # 기본 위치 또는 오류 처리
                x, y = BOARD_EDGES['left'], BOARD_EDGES['top']  # 임시 위치
                corner_block_found = True  # 이 로직을 벗어나도록 설정

        if corner_block_found and not (x and y):  # 코너로 판정되었으나 x,y가 0이면 기본값
            print(f"Warning: Player position seq {seq} (corner) couldn't find exact CORNER_POSITION.")
            x, y = BOARD_EDGES['left'], BOARD_EDGES['top']

        # --- 임시 플레이어 위치 계산 끝 ---

        return x * scale_factor, y * scale_factor

    def _rotate_point(self, x, y, angle_degrees):
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        return new_x, new_y

    def update_player_position(self, player: Player, position: int):
        pass

    def _calculate_scale_factor(self, screen_width, screen_height):
        screen_diagonal = min(screen_width, screen_height) * 0.95
        original_diagonal = math.sqrt(BOARD_CONTENT_WIDTH ** 2 + BOARD_CONTENT_HEIGHT ** 2)
        scale_factor = screen_diagonal / original_diagonal
        max_scale = min(screen_width / BOARD_CONTENT_WIDTH,
                        screen_height / BOARD_CONTENT_HEIGHT) * 1.5
        return min(scale_factor, max_scale)

    def _scale_board(self, scale_factor):
        scaled_width = max(10, int(self.board_surface.get_width() * scale_factor))
        scaled_height = max(10, int(self.board_surface.get_height() * scale_factor))
        return pygame.transform.smoothscale(self.board_surface, (scaled_width, scaled_height))