import pygame
from enum import Enum


class CornerType(Enum):
    START = "시작점"
    ISLAND = "무인도"
    FESTIVAL = "축제 개최"
    TRAVEL = "슝슝여행"


class CornerBlock:

    def __init__(self, side_length: float, fill_color, outline_color, corner_type: CornerType = None,
                 line_width: int = 1, font=None):
        self.side_length = side_length
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.line_width = line_width
        self.corner_type = corner_type
        self.font = font
        self.rect = pygame.Rect(0, 0, side_length, side_length)

    def draw(self, surface: pygame.Surface, center_x: float, center_y: float):
        self.rect.center = (center_x, center_y)
        pygame.draw.rect(surface, self.fill_color, self.rect)
        pygame.draw.rect(surface, self.outline_color, self.rect, self.line_width)

        if self.corner_type:
            text_surface = self.font.render(self.corner_type.value, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
