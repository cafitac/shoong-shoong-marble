import tkinter as tk
from tkinter import font
from typing import Optional

from app.game.impl import Game
from app.player.impl import Player


class PlayerSetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("슝슝마블")
        self.root.geometry("1080x740")
        self.root.configure(bg='#E5E5E5')

        self.header_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.text_font = font.Font(family="Helvetica", size=12)

        self.game: Optional[Game] = None

        self.num_players = 0
        self.entries = []
        self.players = []

        self.show_player_selection()

    def show_player_selection(self):
        self.clear_widgets()

        self.center_frame = tk.Frame(self.root, bg='#D86B6B', padx=40, pady=30)
        self.center_frame.place(relx=0.5, rely=0.5, anchor='center')

        title_label = tk.Label(self.center_frame, text="숭숭마블", bg='#D86B6B', fg='white', font=self.header_font)
        title_label.pack(pady=(0, 5))

        info_label = tk.Label(self.center_frame, text="플레이어 인원 수를 선택하세요.", bg='#D86B6B', fg='white',
                              font=self.text_font)
        info_label.pack(pady=(0, 20))

        button_frame = tk.Frame(self.center_frame, bg='#D86B6B')
        button_frame.pack()

        for i in [2, 3, 4]:
            btn = tk.Button(button_frame, text=str(i), command=lambda i=i: self.show_name_input(i),
                            bg='white', fg='#D86B6B', font=self.text_font,
                            width=4, height=2, relief='flat', bd=0, highlightthickness=0)
            btn.pack(side='left', padx=10)

    def add_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.config(fg='grey')

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, 'end')
                entry.config(fg='black')

        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(fg='grey')

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def show_name_input(self, player_count):
        self.clear_widgets()
        self.num_players = player_count
        self.entries = []

        self.input_frame = tk.Frame(self.root, bg='#D86B6B', padx=40, pady=30)
        self.input_frame.place(relx=0.5, rely=0.5, anchor='center')

        top_frame = tk.Frame(self.input_frame, bg='#D86B6B')
        top_frame.pack(fill='x', anchor='w')

        back_btn = tk.Button(top_frame, text="←", command=self.show_player_selection,
                             bg='#D86B6B', fg='black', font=self.text_font,
                             relief='flat', bd=0, highlightthickness=0)
        back_btn.pack(anchor='w')

        for i in range(player_count):
            row = tk.Frame(self.input_frame, bg='#D86B6B')
            row.pack(pady=5)

            label = tk.Label(row, text=f"플레이어 {i + 1}", bg='#D86B6B', fg='white', font=self.text_font, width=10,
                             anchor='e')
            label.pack(side='left')

            entry = tk.Entry(row, font=self.text_font, width=30, relief='flat', bg='white')
            self.add_placeholder(entry, "닉네임을 입력해주세요.")
            entry.pack(side='left', padx=10)

            self.entries.append(entry)

        finish_btn = tk.Button(self.input_frame, text="게임시작", command=self.on_submit,
                               bg='white', fg='#D86B6B', font=self.text_font,
                               relief='flat', bd=0, highlightthickness=0)
        finish_btn.pack(pady=(20, 0), anchor='e')

    def on_submit(self):
        self.players.clear()
        players = []
        for idx, entry in enumerate(self.entries):
            name = entry.get()
            if name != "닉네임을 입력해주세요.":
                players.append(Player(idx + 1, name))
            else:
                players.append(Player(idx + 1, f"Player {idx + 1}"))

        self.game = Game(players)
        self.show_game_screen()

    def show_game_screen(self):
        self.clear_widgets()

        current_players = self.game.get_players()
        sorted_players = sorted(current_players, key=lambda p: p.get_asset(), reverse=True)
        positions = [(0.01, 0.01), (0.01, 0.85), (0.75, 0.85), (0.75, 0.01)]

        for idx, player in enumerate(sorted_players):
            frame = tk.Frame(self.root, bg='#7586EB', padx=20, pady=10)
            x, y = positions[idx]
            frame.place(relx=x, rely=y)

            name_label = tk.Label(frame, text=player.get_name(), bg='#7586EB', fg='white', font=self.text_font,
                                  anchor='w')
            name_label.pack(anchor='w')

            rank_circle = tk.Label(frame, text=f"{idx + 1}위", bg='#3B3280', fg='white', font=self.text_font, width=4)
            rank_circle.pack(anchor='e', pady=(0, 5))

            cash_label = tk.Label(frame, text=f"보유 현금 : {player.get_cash()}", bg='#7586EB', fg='white',
                                  font=self.text_font)
            cash_label.pack(anchor='w')

            asset_label = tk.Label(frame, text=f"보유 자산 : {player.get_asset()}", bg='#7586EB', fg='white',
                                   font=self.text_font)
            asset_label.pack(anchor='w')

        # 주사위 굴리기 버튼 추가
        dice_button = tk.Button(self.root, text="주사위 굴리기",
                                command=self.roll_dice,
                                bg='white', fg='#D86B6B',
                                font=self.text_font)
        dice_button.place(relx=0.5, rely=0.5, anchor='center')

    def roll_dice(self):
        current_player = self.game.get_current_player()
        dice_result = self.game.roll_dices()

        # 주사위 결과를 화면에 표시
        result_label = tk.Label(self.root,
                                text=f"{current_player.get_name()}의 주사위 결과: {dice_result}",
                                bg='#E5E5E5', fg='black',
                                font=self.text_font)
        result_label.place(relx=0.5, rely=0.6, anchor='center')

        # 게임 상태 업데이트
        self.update_game_state()

    def update_game_state(self):
        # 게임 상태가 변경될 때마다 화면 갱신
        self.show_game_screen()

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerSetupApp(root)
    root.mainloop()
