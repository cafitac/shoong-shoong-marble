# board_renderer.py
import pygame
import math

from ui.board_block import BoardBlock
from constants import *
from corner_block import CornerBlock, CornerType


class BoardRenderer:
    def __init__(self, board_surface, fonts, colors):
        self.board_surface = board_surface
        self.fonts = fonts
        self.colors = colors
        self.rotation_angle = 45
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

        self.main_block = BoardBlock(
            CELL_SHORT, CELL_LONG,
            sample_texts_pg,
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
        current_w, current_h = screen.get_size()
        scale_factor = self._calculate_scale_factor(current_w, current_h)
        scaled_board = self._scale_board(scale_factor)
        rotated_board = pygame.transform.rotate(scaled_board, self.rotation_angle)
        rect = rotated_board.get_rect(center=(center_x, center_y))
        screen.blit(rotated_board, rect)

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
