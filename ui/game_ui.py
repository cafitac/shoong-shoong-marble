# game_ui.py
import pygame
import math

from config.ui_config import UIConfig
from constants import *
from board_renderer import BoardRenderer
from player_panel import PlayerPanel
from ui.components.button import Button


class GameUI:

    def __init__(self):
        pygame.init()
        self.screen = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.fonts = self._init_fonts()
        self._init_screen()
        self.board_renderer = None  # 초기에는 None으로 설정

        # PlayerPanel 색상 설정
        self.player_panel_colors = {
            'background': COLOR_PLAYER_PANEL_BG,
            'rank_badge': COLOR_PLAYER_RANK_BG,
            'text': COLOR_WHITE
        }

        self.player_panel = PlayerPanel(self.fonts, self.player_panel_colors)

        self._init_ui_elements()

    def _init_fonts(self):
        try:
            fonts = {
                'main': pygame.font.Font(FONT_PATH_BOLD, ref_main_font_size),
                'price': pygame.font.Font(FONT_PATH_REGULAR, ref_price_font_size),
                'player_name': pygame.font.Font(FONT_PATH_BOLD, ref_player_name_font_size),
                'player_info': pygame.font.Font(FONT_PATH_REGULAR, ref_player_info_font_size),
                'player_rank': pygame.font.Font(FONT_PATH_BOLD, ref_player_rank_font_size),
                'corner': pygame.font.Font(FONT_PATH_BOLD, ref_corner_font_size)  # 코너 블록용 폰트 추가
            }
        except pygame.error as e:
            print(f"나눔고딕 폰트 파일을 로드할 수 없습니다: {e}. 기본 시스템 폰트를 사용합니다.")
            fonts = {
                'main': pygame.font.SysFont("Arial", ref_main_font_size),
                'price': pygame.font.SysFont("Arial", ref_price_font_size),
                'player_name': pygame.font.SysFont("Arial", ref_player_name_font_size, bold=True),
                'player_info': pygame.font.SysFont("Arial", ref_player_info_font_size),
                'player_rank': pygame.font.SysFont("Arial", ref_player_rank_font_size, bold=True),
                'corner': pygame.font.SysFont("Arial", ref_corner_font_size, bold=True)  # 코너 블록용 폰트 추가
            }
        return fonts

    def _init_screen(self):
        try:
            screen_info = pygame.display.Info()
            screen_width = screen_info.current_w
            screen_height = screen_info.current_h
            screen_flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            self.screen = pygame.display.set_mode((screen_width, screen_height), screen_flags)
        except Exception as e:
            print(f"전체 화면 설정 실패: {e}. 기본 크기(1280x800)로 설정합니다.")
            self.screen = pygame.display.set_mode((1280, 800), pygame.RESIZABLE)
        pygame.display.set_caption("슝슝마블 Pygame (보드 크기 최대화)")

    def _init_board_renderer(self, game):
        board_surface = pygame.Surface((BOARD_CONTENT_WIDTH, BOARD_CONTENT_HEIGHT), pygame.SRCALPHA)
        board_surface.fill(COLOR_BOARD_BG_UNROTATED)

        board = game.get_board()
        board_spaces = board.get_spaces()
        position_manager = game.get_position_manager()  # PositionManager 가져오기

        return BoardRenderer(
            board_surface=board_surface,
            fonts=self.fonts,
            colors=BLOCK_COLORS,
            board_spaces=board_spaces,
            position_manager=position_manager  # PositionManager 전달
        )

    def _init_ui_elements(self):
        self.dice_result_text = ""
        self._init_buttons()

    def _init_buttons(self):
        self.dice_button = Button(
            UIConfig.DICE_BUTTON_RECT,
            "주사위 굴리기",
            self.fonts.get("main"),
            UIConfig.BUTTON_COLOR,
            UIConfig.BUTTON_TEXT_COLOR
        )

    def _handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.dice_button.is_clicked(event.pos):
                    # 버튼 비활성화
                    self.dice_button.enabled = False
                    
                    # 주사위 굴리기
                    dice_result = game.roll_dices() 
                    self.dice_result_text = ", ".join(str(d) for d in dice_result)
                    
                    # 플레이어 이동
                    player = game.get_current_player()
                    game.get_position_manager().move(player, sum(dice_result))
                    arrival_space = game.get_position_manager().get_location(player)
                    print(f"{player.get_name()}이 {sum(dice_result)}칸 이동 > {arrival_space.get_name()} 도착")
                    arrival_space.on_land(player)
                    
                    # 다음 턴 넘기기
                    game.get_turn_manager().next()
                    
                    # 버튼 활성화
                    self.dice_button.enabled = True

    def run(self, game):
        # game 객체를 _init_board_renderer에 전달
        self.board_renderer = self._init_board_renderer(game)

        while self.running:
            self._handle_events(game)
            self.screen.fill(COLOR_SCREEN_BG)

            current_w, current_h = self.screen.get_size()
            self.board_renderer.draw_board(self.screen, current_w / 2, current_h / 2)

            # 플레이어 패널 그리기
            player_positions = self.player_panel.calculate_positions(current_w, current_h)
            for i, player in enumerate(game.get_players()):
                rank = i + 1
                if rank in player_positions:
                    self.player_panel.draw(self.screen, player, rank, player_positions[rank])

            self.dice_button.draw(self.screen)
            dice_label = self.fonts["main"].render(self.dice_result_text, True, UIConfig.TEXT_COLOR)
            self.screen.blit(dice_label, (UIConfig.LABEL_X_DICE, UIConfig.LABEL_Y_DICE))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

