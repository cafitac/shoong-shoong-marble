from app.dice.dices import Dices


def main():
    dices: Dices = Dices(count=2)
    print(dices.roll())


if __name__ == '__main__':
    main()
