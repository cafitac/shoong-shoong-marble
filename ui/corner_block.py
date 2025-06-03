import pygame
from app.board_space.abstract import BoardSpace


class CornerBlock:
    def __init__(self, side_length: float, fill_color, outline_color,
                 space: BoardSpace, line_width: int = 1, font=None):
        self.side_length = side_length
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.line_width = line_width
        self.space = space
        self.font = font
        self.rect = pygame.Rect(0, 0, side_length, side_length)

    def draw(self, surface: pygame.Surface, center_x: float, center_y: float):
        self.rect.center = (center_x, center_y)
        pygame.draw.rect(surface, self.fill_color, self.rect)
        pygame.draw.rect(surface, self.outline_color, self.rect, self.line_width)

        if self.font:
            text_surface = self.font.render(self.space._name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)