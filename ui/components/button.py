# ui/components.py
import pygame


class Button:
    def __init__(self, rect, text, font, bg_color, text_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.enabled = True

    def draw(self, surface):
        color = self.bg_color if self.enabled else tuple(int(c * 0.5) for c in self.bg_color)
        pygame.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)
