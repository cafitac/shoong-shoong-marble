# game_ui.py
import pygame
import math

from config.ui_config import UIConfig
from constants import *
from ui.board_renderer import BoardRenderer
from ui.player_panel import PlayerPanel
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

        # 버튼 초기화는 화면 크기를 알아야 해서 여기서는 하지 않음
        self.dice_button = None
        self.dice_result_text = ""

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

    def _update_dice_button_position(self, screen_width, screen_height):
        # 주사위 버튼 크기 설정
        button_width = 180
        button_height = 60

        # 화면 중앙에 버튼 위치 계산
        button_x = (screen_width - button_width) // 2
        button_y = (screen_height - button_height) // 2

        # 버튼 생성 또는 업데이트
        if self.dice_button is None:
            self.dice_button = Button(
                (button_x, button_y, button_width, button_height),
                "주사위 굴리기",
                self.fonts.get("main"),
                UIConfig.BUTTON_COLOR,
                UIConfig.BUTTON_TEXT_COLOR
            )
        else:
            self.dice_button.rect = pygame.Rect(button_x, button_y, button_width, button_height)

    def _handle_dice_roll(self, game):
        # 주사위 굴리기
        dice_result = game.roll_dices()
        self.dice_result_text = f"주사위: {', '.join(str(d) for d in dice_result)} = {sum(dice_result)}"

        # 현재 플레이어 가져오기
        current_player = game.get_current_player()

        # 플레이어가 턴이 차단된 상태인지 확인
        if current_player.is_turn_blocked():
            # 차단된 턴 처리 - 다음 턴으로 진행
            current_player.next_turn()
            print(f"{current_player.get_name()}의 턴이 차단되었습니다. 남은 차단 턴: {current_player._turns_to_wait}")

            # 턴 매니저를 사용하여 다음 플레이어로 넘기기
            game.get_turn_manager().next()
            return

        # position_manager를 통해 플레이어 이동
        position_manager = game.get_position_manager()
        position_manager.move(current_player, sum(dice_result))

        # 도착한 위치 정보 가져오기
        arrival_space = position_manager.get_location(current_player)
        print(f"{current_player.get_name()}이 {sum(dice_result)}칸 이동 > {arrival_space.get_name()} 도착")

        # 도착한 칸의 효과 발동
        arrival_space.on_land(current_player)

        # 턴 매니저를 통해 다음 플레이어로 턴 전환
        game.get_turn_manager().next()

    def _handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self._update_dice_button_position(event.w, event.h)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.dice_button and self.dice_button.is_clicked(event.pos):
                    # 버튼 비활성화
                    self.dice_button.enabled = False

                    # 주사위 굴리기 및 플레이어 이동 처리
                    self._handle_dice_roll(game)

                    # 버튼 활성화
                    self.dice_button.enabled = True

    def run(self, game):
        # game 객체를 _init_board_renderer에 전달
        self.board_renderer = self._init_board_renderer(game)

        while self.running:
            current_w, current_h = self.screen.get_size()

            # 화면 크기에 따라 주사위 버튼 위치 업데이트
            self._update_dice_button_position(current_w, current_h)

            self._handle_events(game)
            self.screen.fill(COLOR_SCREEN_BG)

            # 보드 그리기
            self.board_renderer.draw_board(self.screen, current_w / 2, current_h / 2)

            # 플레이어 패널 그리기
            player_positions = self.player_panel.calculate_positions(current_w, current_h)
            for i, player in enumerate(game.get_players()):
                rank = i + 1
                if rank in player_positions:
                    self.player_panel.draw(self.screen, player, rank, player_positions[rank])

            # 주사위 버튼 그리기
            if self.dice_button:
                self.dice_button.draw(self.screen)

            # 주사위 결과 표시
            if self.dice_result_text:
                dice_label = self.fonts["main"].render(self.dice_result_text, True, COLOR_WHITE)
                dice_label_rect = dice_label.get_rect(center=(current_w / 2, (current_h / 2) + 50))
                self.screen.blit(dice_label, dice_label_rect)

            # 현재 플레이어 표시
            current_player = game.get_current_player()
            if current_player:
                player_turn_text = f"현재 차례: {current_player.get_name()}"
                player_turn_label = self.fonts["main"].render(player_turn_text, True, COLOR_WHITE)
                player_turn_rect = player_turn_label.get_rect(center=(current_w / 2, (current_h / 2) - 50))
                self.screen.blit(player_turn_label, player_turn_rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()