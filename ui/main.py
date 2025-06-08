import pygame
from app.game.impl import Game
from app.player.impl import Player
from config.ui_config import UIConfig
from game.states import GameState
from ui.game_ui import GameUI
from ui.constants import *
from ui.components.button import Button
from ui.components.input_field import InputField


class PlayerSetupUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(UIConfig.SCREEN_SIZE)
        pygame.display.set_caption("슝슝마블")

        self._init_state()
        self._init_fonts()
        self._init_ui_elements()

    def _init_state(self):
        self.state = GameState.PLAYER_COUNT
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_count = 0
        self.input_fields = []

    def _init_fonts(self):
        try:
            self.title_font = pygame.font.Font(FONT_PATH_BOLD, UIConfig.TITLE_FONT_SIZE)
            self.button_font = pygame.font.Font(FONT_PATH_BOLD, UIConfig.BUTTON_FONT_SIZE)
        except pygame.error:
            self.title_font = pygame.font.SysFont("Arial", UIConfig.TITLE_FONT_SIZE)
            self.button_font = pygame.font.SysFont("Arial", UIConfig.BUTTON_FONT_SIZE)

    def _init_ui_elements(self):
        self._init_player_count_buttons()
        self._init_navigation_buttons()

    def _init_player_count_buttons(self):
        self.player_count_buttons = [
            Button(
                (UIConfig.BUTTON_START_X, UIConfig.BUTTON_START_Y + i * UIConfig.BUTTON_SPACING,
                 UIConfig.BUTTON_WIDTH, UIConfig.BUTTON_HEIGHT),
                str(i + 2),
                self.title_font,
                UIConfig.BUTTON_COLOR,
                UIConfig.BUTTON_TEXT_COLOR
            ) for i in range(3)
        ]

    def _init_navigation_buttons(self):
        self.back_button = Button(
            UIConfig.BACK_BUTTON_RECT,
            "←",
            self.button_font,
            UIConfig.BUTTON_COLOR,
            UIConfig.BLACK_COLOR
        )

        self.start_button = Button(
            UIConfig.START_BUTTON_RECT,
            "게임시작",
            self.button_font,
            UIConfig.BUTTON_COLOR,
            UIConfig.BUTTON_TEXT_COLOR
        )

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        return self.create_game()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == GameState.PLAYER_COUNT:
                self.handle_player_count_events(event)
            else:
                self.handle_name_input_events(event)

    def draw(self):
        self.screen.fill(UIConfig.BG_COLOR)
        if self.state == GameState.PLAYER_COUNT:
            self.draw_player_count_screen()
        else:
            self.draw_name_input_screen()

    def handle_player_count_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_player_count_click(event.pos)

    def _handle_player_count_click(self, pos):
        for i, button in enumerate(self.player_count_buttons):
            if button.is_clicked(pos):
                self._select_player_count(i + 2)

    def _select_player_count(self, count):
        self.player_count = count
        self.state = GameState.NAME_INPUT
        self._create_input_fields()

    def _create_input_fields(self):
        self.input_fields = [
            InputField(
                (UIConfig.INPUT_FIELD_START_X,
                 UIConfig.INPUT_FIELD_START_Y + i * UIConfig.INPUT_FIELD_SPACING,
                 UIConfig.INPUT_FIELD_WIDTH,
                 UIConfig.INPUT_FIELD_HEIGHT),
                "닉네임을 입력해주세요",
                self.button_font,
                UIConfig.INPUT_ACTIVE_COLOR,
                UIConfig.BUTTON_COLOR,
                UIConfig.BLACK_COLOR
            ) for i in range(self.player_count)
        ]

    def handle_name_input_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_name_input_click(event.pos)
        for field in self.input_fields:
            field.handle_event(event)

    def _handle_name_input_click(self, pos):
        if self.back_button.is_clicked(pos):
            self.state = GameState.PLAYER_COUNT
        elif self.start_button.is_clicked(pos):
            self.running = False

    def draw_player_count_screen(self):
        # 제목 텍스트
        title = self.title_font.render("슝슝마블", True, UIConfig.TEXT_COLOR)
        self.screen.blit(title, UIConfig.TITLE_POS)

        subtitle = self.button_font.render("플레이어 인원 수를 선택하세요", True, UIConfig.TEXT_COLOR)
        self.screen.blit(subtitle, UIConfig.SUBTITLE_POS)

        # 버튼 그리기
        for button in self.player_count_buttons:
            button.draw(self.screen)

    def draw_name_input_screen(self):
        self.back_button.draw(self.screen)

        for i, field in enumerate(self.input_fields):
            # 플레이어 라벨
            label = self.button_font.render(f"플레이어 {i + 1}", True, UIConfig.TEXT_COLOR)
            self.screen.blit(label, (UIConfig.LABEL_X, UIConfig.LABEL_Y_START + i * UIConfig.LABEL_Y_SPACING))
            field.draw(self.screen)

        self.start_button.draw(self.screen)

    def create_game(self):
        if not self.player_count:
            return None

        players = []
        for i, field in enumerate(self.input_fields):
            name = field.text.strip() or f"플레이어{i + 1}"
            players.append(Player(i, name))
        return Game(players)


def main():
    try:
        setup_ui = PlayerSetupUI()
        game = setup_ui.run()

        if game:
            ui = GameUI()
            ui.run(game)
    except Exception as e:
        print(f"게임 실행 중 오류가 발생했습니다: {e}")
        pygame.quit()
