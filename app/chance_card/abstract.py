from abc import ABC, abstractmethod
from typing import Any


class ChangeCard(ABC):

    @abstractmethod
    def use(self) -> Any:
        ...
