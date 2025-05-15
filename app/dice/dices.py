from app.dice.impl import Dice


class Dices:
    datas: list[Dice]

    def __init__(self, count: int) -> None:
        self.datas = [Dice(faces=6) for _ in range(count)]

    def roll(self) -> list[int]:
        results: list[int] = []
        for data in self.datas:
            results.append(data.roll())

        return results

