from app.board_space.abstract import BoardSpace
from app.player.impl import Player
import random

class BonusGameSpace(BoardSpace):

    def on_land(self, player: Player):
        print(f"{player}님이 보너스 게임에 도착했습니다.")
        print("보너스 게임을 시작합니다.")
        
        bet_options = [100_000, 200_000, 300_000]
        while True:
            try:
                bet = int(input(f"배팅 금액을 선택하세요 {bet_options} : "))
                if bet in bet_options and player.money >= bet:
                    break
                else:
                    print("잘못된 금액이거나 잔액이 부족합니다.")
            except ValueError:
                print("숫자를 입력하세요.")

        player.money -= bet
        print(f"{bet}원을 배팅하셨습니다. 게임을 시작합니다.")

        rewards = [2, 4, 8] # 각 라운드의 보상 배수
        for round_num in range(3):
            # TODO : 앞, 뒤 버튼을 사용하여 동전의 앞/뒤를 맞추는 로직으로 변경이 필요합니다.
            answer = input("동전의 앞/뒤를 맞춰보세요 (앞/뒤, stop 입력시 중단): ")
            if answer == "stop":
                print("게임을 중단합니다.")
                player.money += bet * rewards[round_num]
                print(f"보상: {bet * rewards[round_num]}원 지급!")
                return
            coin = random.choice(["앞", "뒤"])
            print(f"동전 결과: {coin}")
            if answer == coin:
                print("정답입니다!")
                if round_num == 2:
                    player.money += bet * rewards[round_num]
                    print(f"최대 라운드 성공! 보상: {bet * rewards[round_num]}원 지급!")
                    return
            else:
                print("틀렸습니다. 보너스는 없습니다.")
                return
