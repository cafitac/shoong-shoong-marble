import pygame
import math

from app.board_space.abstract import BoardSpace
from app.board_space.property.impl import PropertySpace


class BoardBlock:
    def __init__(self, width: float, height: float,
                 space: BoardSpace, colors: dict, fonts: dict,
                 upper_part_height_ratio: float = 0.75,
                 lower_part_width_factor: float = 1.0,
                 player_space_ratio_in_upper: float = 0.30):
        self.width = width
        self.height = height
        self.colors = colors
        self.fonts = fonts
        self.upper_part_height_ratio = upper_part_height_ratio
        self.lower_part_width_factor = lower_part_width_factor
        self.player_space_ratio_in_upper = player_space_ratio_in_upper
        self.space = space
        self.texts = self._init_texts()

    def _init_texts(self) -> dict:
        texts = {
            'seq': str(self.space.get_seq()),  # seq 정보 추가
            'name': self.space.get_name(),
            'level': '',
            'price': ''
        }

        if isinstance(self.space, PropertySpace):
            building = self.space.get_building()
            texts['level'] = str(building.get_level()) if building else ''
            texts['price'] = str(building.get_price()) if building else ''

        return texts

    def _rotate_point(self, px, py, cx, cy, angle_degrees):
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        nx = cx + (px - cx) * cos_a - (py - cy) * sin_a
        ny = cy + (px - cx) * sin_a + (py - cy) * cos_a
        return (nx, ny)

    def _draw_upper_part(self, surface, center_x, center_y, angle):
        half_w, half_h = self.width / 2, self.height / 2
        upper_height = self.height * self.upper_part_height_ratio
        y_division = -half_h + upper_height

        # 상단부 꼭지점 계산
        local_corners = [
            (-half_w, -half_h),
            (half_w, -half_h),
            (half_w, y_division),
            (-half_w, y_division)
        ]

        # 회전 및 위치 적용
        world_corners = [self._rotate_point(px, py, 0, 0, angle) for px, py in local_corners]
        world_corners = [(center_x + wx, center_y + wy) for wx, wy in world_corners]

        pygame.draw.polygon(surface, self.colors['upper_bg'], world_corners)
        pygame.draw.polygon(surface, self.colors['outline'], world_corners, 1)

    def _draw_lower_part(self, surface, center_x, center_y, angle):
        half_w, half_h = self.width / 2, self.height / 2
        upper_height = self.height * self.upper_part_height_ratio
        y_division = -half_h + upper_height
        lower_width = self.width * self.lower_part_width_factor
        lower_half_w = lower_width / 2

        # 하단부 꼭지점 계산
        local_corners = [
            (-lower_half_w, y_division),
            (lower_half_w, y_division),
            (lower_half_w, half_h),
            (-lower_half_w, half_h)
        ]

        # 회전 및 위치 적용
        world_corners = [self._rotate_point(px, py, 0, 0, angle) for px, py in local_corners]
        world_corners = [(center_x + wx, center_y + wy) for wx, wy in world_corners]

        pygame.draw.polygon(surface, self.colors['lower_bg'], world_corners)
        pygame.draw.polygon(surface, self.colors['outline'], world_corners, 1)

    def _draw_rotated_text(self, surface, center_x, center_y, angle, text, x_offset, y_offset, font, color):
        rotated_x, rotated_y = self._rotate_point(x_offset, y_offset, 0, 0, angle)
        text_surface = font.render(text, True, color)
        rotated_text = pygame.transform.rotate(text_surface, -angle)
        text_rect = rotated_text.get_rect(center=(center_x + rotated_x, center_y + rotated_y))
        surface.blit(rotated_text, text_rect)

    def _draw_texts(self, surface, center_x, center_y, angle):
        half_h = self.height / 2
        upper_height = self.height * self.upper_part_height_ratio
        player_space_height = upper_height * self.player_space_ratio_in_upper
        text_area_total_height = upper_height * (1.0 - self.player_space_ratio_in_upper)

        # 텍스트 영역의 시작 y좌표 (상단 경계 기준)
        text_area_start_y = -half_h + player_space_height

        main_font = self.fonts['main']
        price_font = self.fonts['price']
        line_height = main_font.get_height()
        gap = line_height * 0.15  # 간격을 조금 줄임

        # 세 줄 텍스트 (seq, level, name)를 위한 y 위치 계산
        # 텍스트 영역의 수직 중앙을 기준으로 배치
        text_block_center_y = text_area_start_y + text_area_total_height / 2

        seq_text = self.texts.get('seq', '')
        level_text = self.texts.get('level', '')
        name_text = self.texts.get('name', '')

        # Seq 텍스트
        seq_y = text_block_center_y - line_height - gap
        self._draw_rotated_text(surface, center_x, center_y, angle,
                                f"[{seq_text}]", 0, seq_y,
                                main_font, self.colors['text'])

        # 레벨 텍스트
        level_y = text_block_center_y
        self._draw_rotated_text(surface, center_x, center_y, angle,
                                level_text, 0, level_y,
                                main_font, self.colors['text'])

        # 이름 텍스트
        name_y = text_block_center_y + line_height + gap
        self._draw_rotated_text(surface, center_x, center_y, angle,
                                name_text, 0, name_y,
                                main_font, self.colors['text'])

        # 가격 텍스트 (하단부 중앙)
        price_y = -half_h + upper_height + (self.height - upper_height) / 2
        self._draw_rotated_text(surface, center_x, center_y, angle,
                                self.texts.get('price', ''), 0, price_y,
                                price_font, self.colors['text'])

    def draw(self, surface: pygame.Surface, center_x: float, center_y: float, angle: float):
        self._draw_upper_part(surface, center_x, center_y, angle)
        self._draw_lower_part(surface, center_x, center_y, angle)
        self._draw_texts(surface, center_x, center_y, angle)
