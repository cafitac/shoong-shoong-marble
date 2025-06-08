from typing import Optional, Callable


class LandResult:
    def __init__(self, message: str, actions: list[str], callback: Optional[Callable[[str], Optional["LandResult"]]] = None, is_prompt: bool = False, on_complete_seq=None):
        self.message = message
        self.actions = actions
        self.callback = callback
        self.is_prompt = is_prompt
        self.on_complete_seq = on_complete_seq
