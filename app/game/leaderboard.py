from typing import List
from app.player.impl import Player

class LeaderBoard:
    def __init__(self, players: List[Player]):
        self.all_players = players
        self.bankrupt_players: List[Player] = []

    def mark_bankrupt(self, player: Player):
        if player not in self.bankrupt_players:
            self.bankrupt_players.append(player)

    def get_rank(self) -> List[Player]:
        survivors = [p for p in self.all_players if p not in self.bankrupt_players]
        full_ranking = self.bankrupt_players + survivors
        return full_ranking[::-1]

    def print_rank(self):
        ranked_players = self.get_rank()
        print("최종 순위")
        for idx, player in enumerate(ranked_players, 1):
            print(f"{idx}등: {player.get_name()}")
