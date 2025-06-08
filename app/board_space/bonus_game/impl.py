from app.board_space.abstract import BoardSpace
from app.board_space.land_result import LandResult
from app.player.impl import Player
import random

class BonusGameSpace(BoardSpace):

    def on_land(self, player: Player):
        print(f"{player}님이 보너스 게임에 도착했습니다.")
        print("보너스 게임을 시작합니다.")
        
        bet_options = [100, 200, 300]
        bet_options = [b for b in bet_options if player.get_cash().amount >= b]

        if player.get_cash().amount < min(bet_options):
            return LandResult("현금이 부족하여 보너스 게임을 진행할 수 없습니다.", ["OK"], lambda _: None)

        def handle_bet(bet_str: str):
            bet = int(bet_str)

            player.get_cash().amount -= bet
            print(f"{bet}원을 배팅하셨습니다. 게임을 시작합니다.")
            return self.play_game(player, bet, 0)  # 라운드 0부터 시작

        return LandResult(
            "배팅 금액을 선택하세요.",
            [str(b) for b in bet_options],
            handle_bet
        )

    def play_game(self, player: Player, bet: int, round_num: int):
        rewards = [2, 4, 8]  # 각 라운드의 보상 배수

        def handle_guess(guess: str):
            if guess == "STOP":
                player.get_cash().amount += bet * rewards[round_num]
                return LandResult(f"게임을 중단합니다.\n보상: {bet * rewards[round_num]}원 지급!", ["OK"], lambda _: None)

            coin = random.choice(["앞", "뒤"])
            print(f"동전 결과: {coin}")

            if guess == coin:
                print("정답입니다!")
                if round_num == 2:
                    player.get_cash().amount += bet * rewards[round_num]
                    return LandResult(f"최대 라운드 성공!\n보상: {bet * rewards[round_num]}원 지급!", ["OK"], lambda _: None)
                else:
                    return self.play_game(player, bet, round_num + 1)  # 다음 라운드
            else:
                return LandResult("틀렸습니다. 보너스는 없습니다.", ["OK"], lambda _: None)

        return LandResult(
            f"{round_num + 1}라운드: 동전의 앞/뒤를 맞춰보세요 (앞/뒤, stop 시 중단)",
            ["앞", "뒤", "STOP"],
            handle_guess
        )