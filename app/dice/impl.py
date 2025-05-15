import random
import secrets
from typing import Optional, Sequence, Union


class Dice:
    faces = Union[int, Sequence[int]]

    def __init__(self, faces: int = 6) -> None:
        if faces < 2:
            raise ValueError("주사위의 최소 면 수는 2 입니다.")

        self.faces: tuple[int, ...] = tuple(range(1, faces + 1))
        self._last_result: Optional[int] = None

    def roll(self) -> int:
        self._last_result = secrets.choice(self.faces)
        return self._last_result

    def get_last_result(self) -> int:
        if self._last_result is None:
            raise ValueError("최초 한 번 이상 주사위를 굴려주세요.")

        return self._last_result
