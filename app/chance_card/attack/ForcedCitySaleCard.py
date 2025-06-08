from app.board_space.abstract import BoardSpace
from app.board_space.land_result import LandResult
from app.board_space.property.impl import PropertySpace
from app.chance_card.abstract import ChanceCard, ChanceCardType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game

# 강제 도시 매각
# 지정한 상대 도시 1곳 즉시 매각(건물 파괴)
# 랜드마크는 공격 대상에서 제외
class ForcedCitySaleCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "강제 도시 매각", "지정한 상대 도시 1곳 즉시 매각 (랜드마크 제외)")

    def use(self, game: 'Game'):
        return LandResult(
            message=f"매각할 도시 번호를 입력하세요",
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
            elif target_city.get_owner() is None:
                message = f"해당 도시는 소유자가 없습니다. \n 다른 도시 번호를 입력하세요"

        if message != "":
            return LandResult(
                message=message,
                actions=["OK"],
                callback=lambda new_input: self._handle_city_selection(new_input, city_spaces),
                is_prompt=True
            )

        message = f"{target_city.get_owner().get_name()}의 {target_city.get_name()}이 매각되었습니다."
        target_city.sale_land()

        return LandResult(
            message=message,
            actions=["확인"],
            on_complete_seq=target_city.get_seq()
        )
