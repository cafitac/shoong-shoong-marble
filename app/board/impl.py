from app.board_space.abstract import BoardSpace


class Board:
    _spaces: list[BoardSpace] = []

    def __init__(self, spaces: list[BoardSpace]) -> None:
        for space in spaces:
            if self._spaces and space.get_seq() != self._spaces[-1].get_seq() + 1:
                raise ValueError("보드 순서가 올바르지 않습니다.")
            self._spaces.append(space)
