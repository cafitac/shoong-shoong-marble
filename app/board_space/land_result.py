from typing import Optional, Callable


class LandResult:
    def __init__(self, message: str, actions: list[str], callback: Optional[Callable[[str], Optional["LandResult"]]] = None, is_prompt: bool = False, on_complete_seq=None, player=None, property=None):
        self.message = message
        self.actions = actions
        self.callback = callback
        self.is_prompt = is_prompt
        if isinstance(on_complete_seq, int):
            self.on_complete_seq = [on_complete_seq]
        else:
            self.on_complete_seq = on_complete_seq
        self.player = player
        self.property = property

