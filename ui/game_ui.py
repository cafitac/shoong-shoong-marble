# game_ui.py
import time

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

        # 애니메이션 관련 속성 추가
        self.animation_state = None
        self.dice_result = []
        self.total_steps = 0
        self.current_step = 0
        self.animation_start_time = 0
        self.dice_roll_time = 0
        self.animation_delay = 1  # 주사위 결과 후 2초 대기
        self.step_interval = 0.5  # 1초 간격으로 이동

        # 모달 관련 속성 추가
        self.modal_active = False  # 모달 표시 여부
        self.modal_callback = None  # 모달 콜백 함수
        self.modal_message = "" # 모달 메세지
        self.modal_buttons = []

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
        self.dice_result = game.roll_dices()
        self.total_steps = sum(self.dice_result)
        self.dice_result_text = f"주사위: {', '.join(str(d) for d in self.dice_result)} = {self.total_steps}"

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

        # 애니메이션 시작 설정
        self.animation_state = "waiting"
        self.current_step = 0
        self.dice_roll_time = time.time()
        self.animation_start_time = self.dice_roll_time + self.animation_delay

    def _update_animation(self, game):
        if self.animation_state is None:
            return

        current_time = time.time()

        # 주사위 결과 후 대기
        if self.animation_state == "waiting" and current_time >= self.animation_start_time:
            self.animation_state = "moving"
            self.last_step_time = current_time

        # 한 칸씩 이동
        if self.animation_state == "moving":
            if current_time - self.last_step_time >= self.step_interval and self.current_step < self.total_steps:
                current_player = game.get_current_player()
                position_manager = game.get_position_manager()

                # 현재 위치 가져오기
                old_position = position_manager.get_position(current_player)

                # 한 칸 이동
                new_position = (old_position + 1) % len(game.get_board().get_spaces())
                position_manager.update_player_position(current_player, new_position)

                self.current_step += 1
                self.last_step_time = current_time

                print(
                    f"{current_player.get_name()}이 {old_position}에서 {new_position}로 이동 ({self.current_step}/{self.total_steps})")

            # 모든 이동이 완료된 경우
            elif self.current_step >= self.total_steps:
                current_player = game.get_current_player()
                position_manager = game.get_position_manager()

                # 도착한 위치 정보 가져오기
                arrival_space = position_manager.get_location(current_player)
                print(f"{current_player.get_name()}이 {self.total_steps}칸 이동 > {arrival_space.get_name()} 도착")

                # 도착한 칸의 효과 발동
                btn = pygame.Rect(250, 320, 100, 40)
                result = arrival_space.on_land(current_player)
                if result is not None:
                    msg, actions = result
                    buttons = []
                    for action in actions:
                        if action == "BUILD":
                            buttons.append((BUTTON_LABELS[action], btn, lambda: arrival_space.buy_land(current_player)))
                        elif action == "UPGRADE":
                            buttons.append((BUTTON_LABELS[action], btn, lambda: arrival_space.upgrade_building(current_player)))
                        elif action == "PASS":
                            buttons.append((BUTTON_LABELS[action], btn, lambda: print("패스")))
                        elif action == "OK":
                            buttons.append((BUTTON_LABELS[action], btn, lambda: print("확인")))
                    self.show_modal(message=msg, buttons=buttons)

                # 턴 매니저를 통해 다음 플레이어로 턴 전환
                game.get_turn_manager().next()

                # 애니메이션 상태 초기화
                self.animation_state = None

                # 버튼 활성화
                self.dice_button.enabled = True

    def _handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self._update_dice_button_position(event.w, event.h)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.modal_active:
                    for label, rect, callback in self.modal_buttons:
                        if rect.collidepoint(event.pos):
                            callback()
                            self.modal_active = False
                            break
                else:
                    if self.dice_button and self.dice_button.is_clicked(
                            event.pos) and self.dice_button.enabled and self.animation_state is None:
                        # 버튼 비활성화
                        self.dice_button.enabled = False

                        # 주사위 굴리기 및 애니메이션 준비
                        self._handle_dice_roll(game)

    def show_modal(self, message, buttons):
        self.modal_active = True
        self.modal_message = message
        self.modal_buttons = buttons

    def draw_modal(self):
        screen_width, screen_height = self.screen.get_size()

        # 반투명 배경
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # 모달 박스 크기 및 위치 계산 (가로 50%, 세로 33%)
        modal_width = screen_width * 0.5
        modal_height = screen_height * 0.33
        modal_x = (screen_width - modal_width) / 2
        modal_y = (screen_height - modal_height) / 2
        modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)

        # 모달 박스 그리기
        pygame.draw.rect(self.screen, (255, 255, 255), modal_rect, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), modal_rect, 2)

        # 메시지 출력
        lines = self.modal_message.split('\n')
        for i, line in enumerate(lines):
            label = self.fonts["main"].render(line, True, (0, 0, 0))
            text_x = modal_rect.x + 20
            text_y = modal_rect.y + 20 + i * 30
            self.screen.blit(label, (text_x, text_y))

        # 버튼들 배치 (두 개 기준, 가운데 정렬)
        button_width = 120
        button_height = 40
        button_spacing = 40

        total_button_width = (button_width * len(self.modal_buttons)) + (button_spacing * (len(self.modal_buttons) - 1))
        start_x = (screen_width - total_button_width) / 2
        button_y = modal_rect.bottom - 60

        for i, (label, _, callback) in enumerate(self.modal_buttons):
            btn_x = start_x + i * (button_width + button_spacing)
            rect = pygame.Rect(btn_x, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, (180, 180, 180), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

            text = self.fonts["main"].render(label, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

            # 버튼 rect를 업데이트
            self.modal_buttons[i] = (label, rect, callback)

    def run(self, game):
        # game 객체를 _init_board_renderer에 전달
        self.board_renderer = self._init_board_renderer(game)

        while self.running:
            current_w, current_h = self.screen.get_size()

            # 화면 크기에 따라 주사위 버튼 위치 업데이트
            self._update_dice_button_position(current_w, current_h)

            self._handle_events(game)

            # 애니메이션 업데이트
            self._update_animation(game)

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

                # 애니메이션 중이라면 현재 진행 상태 표시
                if self.animation_state:
                    progress_text = f"이동 중: {self.current_step}/{self.total_steps}"
                    progress_label = self.fonts["main"].render(progress_text, True, COLOR_WHITE)
                    progress_rect = progress_label.get_rect(center=(current_w / 2, (current_h / 2) + 100))
                    self.screen.blit(progress_label, progress_rect)

            # 현재 플레이어 표시
            current_player = game.get_current_player()
            if current_player:
                player_turn_text = f"현재 차례: {current_player.get_name()}"
                player_turn_label = self.fonts["main"].render(player_turn_text, True, COLOR_WHITE)
                player_turn_rect = player_turn_label.get_rect(center=(current_w / 2, (current_h / 2) - 50))
                self.screen.blit(player_turn_label, player_turn_rect)

            # 모달 표시
            if self.modal_active:
                self.draw_modal()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
