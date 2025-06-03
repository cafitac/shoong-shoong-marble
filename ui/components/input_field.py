import pygame


class InputField:
    def __init__(self, rect, placeholder, font, active_color, inactive_color, text_color):
        self.rect = pygame.Rect(rect)
        self.placeholder = placeholder
        self.font = font
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.text_color = text_color
        self.text = ""
        self.active = False

    def draw(self, surface):
        color = self.active_color if self.active else self.inactive_color
        pygame.draw.rect(surface, color, self.rect)
        text_to_render = self.text or self.placeholder
        text_surface = self.font.render(text_to_render, True, self.text_color)
        text_rect = text_surface.get_rect(topleft=(self.rect.x + 10, self.rect.y + 15))
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                self.text += event.unicode
