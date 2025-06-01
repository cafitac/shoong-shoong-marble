# player_panel.py
import pygame


class PlayerPanel:
    def __init__(self, fonts, colors):
        self.fonts = fonts
        self.colors = colors
        self.panel_width = 200  # 패널 기본 너비
        self.panel_height = 120  # 패널 기본 높이
        self.panel_margin = 20  # 패널 간 간격

    def calculate_positions(self, screen_width, screen_height):
        positions = {}
        margin = self.panel_margin

        # 화면 모서리에 패널 배치
        positions[1] = pygame.Rect(  # 좌상단
            margin,
            margin,
            self.panel_width,
            self.panel_height
        )

        positions[2] = pygame.Rect(  # 좌하단
            margin,
            screen_height - self.panel_height - margin,
            self.panel_width,
            self.panel_height
        )

        positions[3] = pygame.Rect(  # 우하단
            screen_width - self.panel_width - margin,
            screen_height - self.panel_height - margin,
            self.panel_width,
            self.panel_height
        )

        positions[4] = pygame.Rect(  # 우상단
            screen_width - self.panel_width - margin,
            margin,
            self.panel_width,
            self.panel_height
        )

        return positions

    def draw(self, surface, player, rank, rect):
        self._draw_background(surface, rect)
        self._draw_player_info(surface, player, rect)
        self._draw_rank_badge(surface, rank, rect)

    def _draw_background(self, surface, rect):
        pygame.draw.rect(surface, self.colors['background'], rect)

    def _draw_player_info(self, surface, player, rect):
        # 폰트 키 이름 수정
        name_font = self.fonts['player_name']
        info_font = self.fonts['player_info']

        # 플레이어 이름
        name_text = name_font.render(player.get_name(), True, self.colors['text'])
        name_rect = name_text.get_rect(topleft=(rect.x + 10, rect.y + 10))
        surface.blit(name_text, name_rect)

        # 현금
        cash_text = info_font.render(f"현금: {player.get_cash()}", True, self.colors['text'])
        cash_rect = cash_text.get_rect(topleft=(rect.x + 10, rect.y + 45))
        surface.blit(cash_text, cash_rect)

        # 자산
        asset_text = info_font.render(f"자산: {player.get_asset()}", True, self.colors['text'])
        asset_rect = asset_text.get_rect(topleft=(rect.x + 10, rect.y + 75))
        surface.blit(asset_text, asset_rect)

    def _draw_rank_badge(self, surface, rank, rect):
        badge_size = 30
        badge_rect = pygame.Rect(
            rect.right - badge_size - 10,
            rect.y + 10,
            badge_size,
            badge_size
        )

        pygame.draw.rect(surface, self.colors['rank_badge'], badge_rect)
        # 폰트 키 이름 수정
        rank_font = self.fonts['player_rank']
        rank_text = rank_font.render(str(rank), True, self.colors['text'])
        rank_rect = rank_text.get_rect(center=badge_rect.center)
        surface.blit(rank_text, rank_rect)
