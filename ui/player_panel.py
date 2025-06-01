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
        # 플레이어 색상으로 반투명 배경 그리기
        background_color = (*player.color, 160)
        background_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(background_surface, background_color, background_surface.get_rect())
        surface.blit(background_surface, rect)

        # 검은색 테두리 그리기
        pygame.draw.rect(surface, (0, 0, 0), rect, 2)

        # 플레이어 이름
        name_text = self.fonts['player_name'].render(player.get_name(), True, (0, 0, 0))
        name_rect = name_text.get_rect(topleft=(rect.x + 10, rect.y + 10))
        surface.blit(name_text, name_rect)

        # 현금 정보
        cash = player.get_cash()
        cash_text = self.fonts['player_info'].render(f"현금: {cash}", True, (0, 0, 0))
        cash_rect = cash_text.get_rect(topleft=(rect.x + 10, rect.y + 45))
        surface.blit(cash_text, cash_rect)

        # 자산 정보
        asset = player.get_asset()
        asset_text = self.fonts['player_info'].render(f"자산: {asset}", True, (0, 0, 0))
        asset_rect = asset_text.get_rect(topleft=(rect.x + 10, rect.y + 75))
        surface.blit(asset_text, asset_rect)

        # 순위 뱃지
        badge_size = 30
        badge_rect = pygame.Rect(
            rect.right - badge_size - 10,
            rect.y + 10,
            badge_size,
            badge_size
        )
        pygame.draw.rect(surface, self.colors['rank_badge'], badge_rect)

        # 순위 숫자
        rank_text = self.fonts['player_rank'].render(str(rank), True, self.colors['text'])
        rank_rect = rank_text.get_rect(center=badge_rect.center)
        surface.blit(rank_text, rank_rect)