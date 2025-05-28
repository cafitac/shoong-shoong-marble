from abc import ABC, abstractmethod
from typing import Any


class ChanceCard(ABC):

    @abstractmethod
    def use(self) -> Any:
        ...
