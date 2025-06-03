import math
import pygame
from typing import Dict, List
from app.player.impl import Player
from app.board_space.abstract import BoardSpace
from ui.board_block import BoardBlock
from ui.corner_block import CornerBlock
from ui.constants import (
    BOARD_CELLS_PER_SIDE,
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
        self.board_spaces = board_spaces
        self.position_manager = position_manager  # PositionManager 추가
        self._init_blocks()
        self._draw_initial_board()

    # BoardRenderer의 _init_blocks 메서드 수정 제안
    def _init_blocks(self):
        # 실제 코너 공간의 seq 값이라고 가정합니다.
        # 이 값들은 board_space_data.csv 또는 관련 설정에서 확인해야 합니다.
        corner_seq_map = {
            "START": 0,
            "ISLAND": 8,
            "FESTIVAL": 16,
            "TRAVEL": 24,
        }

        # seq를 키로 하는 딕셔너리를 만들어 검색을 용이하게 합니다.
        spaces_by_seq = {space.get_seq(): space for space in self.board_spaces}

        corner_spaces = []
        # 정의된 seq 값으로 코너 공간을 찾습니다.
        # 순서를 유지하기 위해 원래 주석에 있던 순서대로 추가합니다.
        start_space = spaces_by_seq.get(corner_seq_map["START"])
        travel_space = spaces_by_seq.get(corner_seq_map["TRAVEL"])  # 주석 순서: TRAVEL이 두 번째 코너
        island_space = spaces_by_seq.get(corner_seq_map["ISLAND"])  # 주석 순서: ISLAND가 세 번째 코너
        festival_space = spaces_by_seq.get(corner_seq_map["FESTIVAL"])  # 주석 순서: FESTIVAL이 네 번째 코너

        # 찾은 공간들을 corner_spaces 리스트에 추가 (None이 아닌 경우)
        # 원래 코드의 corner_spaces 순서를 유지하기 위해 이렇게 구성
        # self.board_spaces[0], self.board_spaces[24], self.board_spaces[8], self.board_spaces[16]
        # 이 순서에 맞춰 추가합니다.
        if start_space: corner_spaces.append(start_space)
        # 다음 코너는 원래 코드에서 self.board_spaces[24] (TRAVEL)로 되어 있었으므로, travel_space를 두 번째로 넣어야 하지만
        # 실제 코너 블록을 그리는 순서(CORNER_POSITIONS)와 매칭되려면 START, ISLAND, FESTIVAL, TRAVEL 순이 맞을 수 있습니다.
        # 여기서는 원래 코드의 인덱스 순서대로 매칭되는 seq를 가정하여 추가합니다.
        # 하지만, 이 부분은 CORNER_POSITIONS와 실제 코너 매핑을 다시 확인해야 할 수 있습니다.
        # 현재는 원본 코드의 인덱스 순서에 해당하는 seq 값의 공간을 넣는다고 가정합니다.
        # (0 -> START, 24 -> TRAVEL, 8 -> ISLAND, 16 -> FESTIVAL)

        # 원래 코드의 corner_spaces 생성 순서에 맞춰 구성
        # self.board_spaces[0] -> START
        # self.board_spaces[24] -> TRAVEL
        # self.board_spaces[8] -> ISLAND
        # self.board_spaces[16] -> FESTIVAL

        _corner_space_candidates_in_original_order = [
            spaces_by_seq.get(corner_seq_map["START"]),  # 원래 인덱스 0
            spaces_by_seq.get(corner_seq_map["TRAVEL"]),  # 원래 인덱스 24
            spaces_by_seq.get(corner_seq_map["ISLAND"]),  # 원래 인덱스 8
            spaces_by_seq.get(corner_seq_map["FESTIVAL"])  # 원래 인덱스 16
        ]

        corner_spaces = [cs for cs in _corner_space_candidates_in_original_order if cs is not None]

        # 코너 블록 초기화
        self.corner_blocks = [
            CornerBlock(
                CORNER_SIDE,
                COLOR_CORNER_FILL,
                COLOR_BLACK,
                space,
                font=self.fonts['corner']
            ) for space in corner_spaces
        ]

        # 일반 블록 초기화 - seq 순서대로 정렬
        # non_corner_spaces를 만들 때, corner_spaces에 실제 객체가 들어있으므로 set으로 만들어 검색 속도 향상
        corner_space_set = set(corner_spaces)
        non_corner_spaces = [space for space in self.board_spaces if space not in corner_space_set]
        non_corner_spaces.sort(key=lambda x: x.get_seq())

        self.board_blocks = [
            BoardBlock(
                CELL_SHORT,
                CELL_LONG,
                space,
                self.colors,
                {'main': self.fonts['main'], 'price': self.fonts['price']}
            ) for space in non_corner_spaces
        ]

    def _draw_initial_board(self):
        # 코너 블록 그리기
        for corner_block, (cx, cy) in zip(self.corner_blocks, CORNER_POSITIONS):
            corner_block.draw(self.board_surface, cx, cy)

        # 메인 블록 그리기
        self._draw_horizontal_blocks()
        self._draw_vertical_blocks()

    def draw_board(self, screen, center_x, center_y):
        # 기본 보드 그리기
        current_w, current_h = screen.get_size()
        scale_factor = self._calculate_scale_factor(current_w, current_h)
        scaled_board = self._scale_board(scale_factor)
        rotated_board = pygame.transform.rotate(scaled_board, self.rotation_angle)
        rect = rotated_board.get_rect(center=(center_x, center_y))
        screen.blit(rotated_board, rect)

        # position_manager가 있는 경우에만 플레이어 그리기
        if self.position_manager:
            self._draw_players(screen, rect, scale_factor)

    def _draw_players(self, screen, board_rect, scale_factor):
        # position_manager에서 모든 플레이어의 위치 정보 가져오기
        for player in self.position_manager._positions.keys():
            position = self.position_manager._positions[player]

            # 플레이어 위치 계산
            pos_coords = self._get_position_coordinates(position, scale_factor)
            if pos_coords:
                x, y = pos_coords

                # 보드의 회전을 고려한 위치 조정
                rotated_x, rotated_y = self._rotate_point(
                    x - board_rect.width / 2,
                    y - board_rect.height / 2,
                    self.rotation_angle
                )
                final_x = rotated_x + board_rect.centerx
                final_y = rotated_y + board_rect.centery

                # 플레이어 그리기
                player_radius = int(CELL_SHORT * scale_factor * 0.15)
                pygame.draw.circle(screen, player.get_color(), (int(final_x), int(final_y)), player_radius)

    def _get_position_coordinates(self, position: int, scale_factor: float) -> tuple[float, float]:
        total_positions = BOARD_CELLS_PER_SIDE * 4 + 4  # 전체 보드 칸 수
        position = position % total_positions

        # 보드의 각 면에 따른 위치 계산
        if position <= BOARD_CELLS_PER_SIDE:  # 아래쪽
            x = BOARD_EDGES['left'] + CORNER_SIDE + (position * CELL_SHORT)
            y = BOARD_EDGES['bottom'] - CELL_LONG / 2
        elif position <= BOARD_CELLS_PER_SIDE * 2 + 1:  # 오른쪽
            x = BOARD_EDGES['right'] - CELL_LONG / 2
            y = BOARD_EDGES['bottom'] - CORNER_SIDE - ((position - BOARD_CELLS_PER_SIDE - 1) * CELL_SHORT)
        elif position <= BOARD_CELLS_PER_SIDE * 3 + 2:  # 위쪽
            x = BOARD_EDGES['right'] - CORNER_SIDE - ((position - BOARD_CELLS_PER_SIDE * 2 - 2) * CELL_SHORT)
            y = BOARD_EDGES['top'] + CELL_LONG / 2
        else:  # 왼쪽
            x = BOARD_EDGES['left'] + CELL_LONG / 2
            y = BOARD_EDGES['top'] + CORNER_SIDE + ((position - BOARD_CELLS_PER_SIDE * 3 - 3) * CELL_SHORT)

        return x * scale_factor, y * scale_factor

    def _rotate_point(self, x, y, angle_degrees):
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        return new_x, new_y

    def update_player_position(self, player: Player, position: int):
        """플레이어의 위치를 업데이트합니다."""
        self.player_positions[player] = position

    def _draw_horizontal_blocks(self):
        # 아래쪽 블록 그리기
        block_index = 0  # 첫 번째 일반 블록(self.board_blocks[0])부터 시작하도록 0으로 변경
        current_x = BOARD_EDGES['left'] + CORNER_SIDE
        center_y = BOARD_EDGES['bottom'] - CELL_LONG / 2

        for _ in range(BOARD_CELLS_PER_SIDE):
            if block_index < len(self.board_blocks):
                center_x = current_x + CELL_SHORT / 2
                self.board_blocks[block_index].draw(self.board_surface, center_x, center_y, 0)
                block_index += 1
            current_x += CELL_SHORT

        # 위쪽 블록 그리기
        current_x = BOARD_EDGES['right'] - CORNER_SIDE
        center_y = BOARD_EDGES['top'] + CELL_LONG / 2

        for _ in range(BOARD_CELLS_PER_SIDE):
            if block_index < len(self.board_blocks):
                center_x = current_x - CELL_SHORT / 2
                self.board_blocks[block_index].draw(self.board_surface, center_x, center_y, 0)
                block_index += 1
            current_x -= CELL_SHORT

    def _draw_vertical_blocks(self):
        block_index = BOARD_CELLS_PER_SIDE * 2  # 수평 블록들 이후부터

        # 왼쪽 블록 그리기
        current_y = BOARD_EDGES['bottom'] - CORNER_SIDE
        center_x = BOARD_EDGES['left'] + CELL_LONG / 2

        for _ in range(BOARD_CELLS_PER_SIDE):
            if block_index < len(self.board_blocks):
                center_y = current_y - CELL_SHORT / 2
                self.board_blocks[block_index].draw(self.board_surface, center_x, center_y, 90)
                block_index += 1
            current_y -= CELL_SHORT

        # 오른쪽 블록 그리기
        current_y = BOARD_EDGES['top'] + CORNER_SIDE
        center_x = BOARD_EDGES['right'] - CELL_LONG / 2

        for _ in range(BOARD_CELLS_PER_SIDE):
            if block_index < len(self.board_blocks):
                center_y = current_y + CELL_SHORT / 2
                self.board_blocks[block_index].draw(self.board_surface, center_x, center_y, 90)
                block_index += 1
            current_y += CELL_SHORT

    def _calculate_scale_factor(self, screen_width, screen_height):
        # 45도 회전된 보드가 화면에 들어갈 수 있는 최대 크기 계산
        screen_diagonal = min(screen_width, screen_height) * 0.95
        original_diagonal = math.sqrt(BOARD_CONTENT_WIDTH ** 2 + BOARD_CONTENT_HEIGHT ** 2)
        scale_factor = screen_diagonal / original_diagonal

        # 최대 스케일 제한
        max_scale = min(screen_width / BOARD_CONTENT_WIDTH,
                        screen_height / BOARD_CONTENT_HEIGHT) * 1.5
        return min(scale_factor, max_scale)

    def _scale_board(self, scale_factor):
        scaled_width = max(10, int(self.board_surface.get_width() * scale_factor))
        scaled_height = max(10, int(self.board_surface.get_height() * scale_factor))
        return pygame.transform.smoothscale(self.board_surface, (scaled_width, scaled_height))
