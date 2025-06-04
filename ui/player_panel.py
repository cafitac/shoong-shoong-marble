# player_panel.py
import pygame
from app.player.impl import Player


class PlayerPanel:
    def __init__(self, fonts, colors):
        self.fonts = fonts
        self.colors = colors
        self.panel_width = 200  # 패널 기본 너비
        self.panel_height = 120  # 패널 기본 높이
        self.panel_margin = 20  # 패널 간 간격

    def calculate_positions(self, screen_width, screen_height):
        """
        화면 크기에 따라 플레이어 패널의 위치를 계산합니다.
        """
        positions = {}
        margin = self.panel_margin

        # 화면 모서리에 패널 배치 (최대 4개의 플레이어 패널)
        panel_positions = [
            (margin, margin),  # 좌상단
            (margin, screen_height - self.panel_height - margin),  # 좌하단
            (screen_width - self.panel_width - margin, screen_height - self.panel_height - margin),  # 우하단
            (screen_width - self.panel_width - margin, margin),  # 우상단
        ]

        for i, pos in enumerate(panel_positions, 1):
            positions[i] = pygame.Rect(
                pos[0], pos[1], self.panel_width, self.panel_height
            )

        return positions

    def draw(self, surface, player, rank, rect):
        """
        플레이어 정보 패널을 그립니다.
        """
        player_color = player.get_color()
        text_color = self._get_contrast_color(player_color)

        # 배경 그리기
        pygame.draw.rect(surface, player_color, rect)

        # 플레이어 정보 그리기
        self._draw_player_info(surface, player, rect, text_color)

        # 랭크 뱃지 그리기
        self._draw_rank_badge(surface, rank, rect)

    def _get_contrast_color(self, bg_color):
        """
        배경색에 따라 적절한 대비색을 반환합니다.
        """
        brightness = (bg_color[0] * 299 + bg_color[1] * 587 + bg_color[2] * 114) / 1000
        return (0, 0, 0) if brightness > 128 else (255, 255, 255)

    def _draw_player_info(self, surface, player, rect, text_color):
        """
        플레이어 이름, 현금, 자산 정보를 그립니다.
        """
        name_font = self.fonts['player_name']
        info_font = self.fonts['player_info']

        # 플레이어 이름
        name_text = name_font.render(player.get_name(), True, text_color)
        name_rect = name_text.get_rect(topleft=(rect.x + 10, rect.y + 10))
        surface.blit(name_text, name_rect)

        # 현금
        cash_text = info_font.render(f"현금: {player.get_cash()}", True, text_color)
        cash_rect = cash_text.get_rect(topleft=(rect.x + 10, rect.y + 45))
        surface.blit(cash_text, cash_rect)

        # 자산
        asset_text = info_font.render(f"자산: {player.get_asset()}", True, text_color)
        asset_rect = asset_text.get_rect(topleft=(rect.x + 10, rect.y + 75))
        surface.blit(asset_text, asset_rect)

    def _draw_rank_badge(self, surface, rank, rect):
        """
        플레이어 순위 뱃지를 그립니다.
        """
        badge_size = 30
        badge_rect = pygame.Rect(
            rect.right - badge_size - 10,
            rect.y + 10,
            badge_size,
            badge_size
        )

        # 랭크 뱃지 배경
        pygame.draw.rect(surface, self.colors['rank_badge'], badge_rect)

        # 랭크 텍스트
        rank_font = self.fonts['player_rank']
        rank_text_color = self._get_contrast_color(self.colors['rank_badge'])
        rank_text = rank_font.render(str(rank), True, rank_text_color)
        rank_rect = rank_text.get_rect(center=badge_rect.center)
        surface.blit(rank_text, rank_rect)