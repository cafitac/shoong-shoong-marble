from app.board_space.abstract import BoardSpace
from app.board_space.property.impl import PropertySpace


class Board:
    _spaces: list[PropertySpace] = []

    def __init__(self, spaces: list[PropertySpace]) -> None:
        for space in spaces:
            if self._spaces and space.get_seq() != self._spaces[-1].get_seq() + 1:
                raise ValueError("보드 순서가 올바르지 않습니다.")
            self._spaces.append(space)

    def get_spaces(self):
        return self._spaces

    def get_city(self, target_city_seq):
        return self._spaces[target_city_seq]

    def get_island(self):
        return self._spaces[8] # TODO: 무인도 위치
