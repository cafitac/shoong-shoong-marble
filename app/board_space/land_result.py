from typing import Optional, Callable


class LandResult:
    def __init__(self, message: str, actions: list[str], callback: Optional[Callable[[str], Optional["LandResult"]]] = None):
        self.message = message
        self.actions = actions
        self.callback = callback
