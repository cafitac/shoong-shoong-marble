import math
import pygame
from typing import Dict, List
from app.player.impl import Player
from app.board_space.abstract import BoardSpace
from ui.board_block import BoardBlock
from ui.corner_block import CornerBlock, CornerType
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


    def _init_blocks(self):
        # 각 코너 블록을 개별적으로 초기화
        self.corner_blocks = [
            CornerBlock(CORNER_SIDE, COLOR_CORNER_FILL, COLOR_BLACK, CornerType.START, font=self.fonts['corner']),
            CornerBlock(CORNER_SIDE, COLOR_CORNER_FILL, COLOR_BLACK, CornerType.TRAVEL, font=self.fonts['corner']),
            CornerBlock(CORNER_SIDE, COLOR_CORNER_FILL, COLOR_BLACK, CornerType.ISLAND, font=self.fonts['corner']),
            CornerBlock(CORNER_SIDE, COLOR_CORNER_FILL, COLOR_BLACK, CornerType.FESTIVAL, font=self.fonts['corner'])
        ]

        # BoardBlock 초기화 시 보드 공간 정보 전달
        self.main_block = BoardBlock(
            CELL_SHORT, CELL_LONG,
            self.board_spaces,  # board_spaces 리스트 전달
            self.colors,
            {'main': self.fonts['main'], 'price': self.fonts['price']}
        )

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
        current_x = BOARD_EDGES['left'] + CORNER_SIDE
        center_y = BOARD_EDGES['bottom'] - CELL_LONG / 2
        for _ in range(BOARD_CELLS_PER_SIDE):
            center_x = current_x + CELL_SHORT / 2
            self.main_block.draw(self.board_surface, center_x, center_y, 0)
            current_x += CELL_SHORT

        # 위쪽 블록 그리기
        current_x = BOARD_EDGES['left'] + CORNER_SIDE
        center_y = BOARD_EDGES['top'] + CELL_LONG / 2
        for _ in range(BOARD_CELLS_PER_SIDE):
            center_x = current_x + CELL_SHORT / 2
            self.main_block.draw(self.board_surface, center_x, center_y, 0)
            current_x += CELL_SHORT

    def _draw_vertical_blocks(self):
        # 왼쪽 블록 그리기
        current_y = BOARD_EDGES['bottom'] - CORNER_SIDE
        center_x = BOARD_EDGES['left'] + CELL_LONG / 2
        for _ in range(BOARD_CELLS_PER_SIDE):
            center_y = current_y - CELL_SHORT / 2
            self.main_block.draw(self.board_surface, center_x, center_y, 90)
            current_y -= CELL_SHORT

        # 오른쪽 블록 그리기
        current_y = BOARD_EDGES['top'] + CORNER_SIDE
        center_x = BOARD_EDGES['right'] - CELL_LONG / 2
        for _ in range(BOARD_CELLS_PER_SIDE):
            center_y = current_y + CELL_SHORT / 2
            self.main_block.draw(self.board_surface, center_x, center_y, 90)
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
