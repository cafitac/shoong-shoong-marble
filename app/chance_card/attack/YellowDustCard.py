from app.board_space.abstract import BoardSpace
from app.board_space.land_result import LandResult
from app.chance_card.abstract import ChanceCard, ChanceCardType
from app.board_space.property.impl import AttackEffectType, PropertySpace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game

# 황사
# 지정 도시 통행료 ½로 하락
class YellowDustCard(ChanceCard):
    def __init__(self, duration: int = 3):
        super().__init__(ChanceCardType.INSTANT, "황사", "지정 도시 통행료 1/2로 하락")
        self.duration = duration
        self.value = 0.5

    def use(self, game: 'Game'):
        return LandResult(
            message=f"황사를 발생시킬 도시 번호를 입력하세요",
            actions=["확인"],
            callback=lambda input_text: self._handle_city_selection(input_text, game.get_board().get_spaces()),
            is_prompt=True
        )

    def _handle_city_selection(self, input_text: str, city_spaces: list[BoardSpace]):
        seq = int(input_text.strip())
        message = ""
        target_city = None

        if seq < 0 or seq > len(city_spaces):
            message = f"잘못된 입력입니다.\n다른 도시 번호를 입력하세요"
        else:
            target_city = city_spaces[seq]
            if not isinstance(target_city, PropertySpace):
                message = f"도시가 아닙니다.\n다른 도시 번호를 입력하세요"
            elif target_city.get_building().is_maxed():
                message = f"{target_city.get_name()}는 이미 랜드마크입니다. \n다른 도시 번호를 입력하세요"

        if message != "":
            return LandResult(
                message=message,
                actions=["OK"],
                callback=lambda new_input: self._handle_city_selection(new_input, city_spaces),
                is_prompt=True
            )

        target_city.set_attack_effect(AttackEffectType.YELLOW_DUST, self.duration, self.value)  # 황사 상태 설정
        return LandResult(
            message=f"{target_city.get_name()}에 황사가 발생했습니다!\n{self.duration}턴 동안 통행료가 1/2로 감소합니다.",
            actions=["확인"]
        )
