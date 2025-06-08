from app.board_space.abstract import BoardSpace
from app.board_space.land_result import LandResult
from app.board_space.property.impl import PropertySpace
from app.chance_card.abstract import ChanceCard, ChanceCardType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.game.impl import Game

# 지진
# 건물 단계 1 단계씩 파괴
# 랜드마크는 공격 대상에서 제외
class EarthquakeCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "지진", "건물 단계 1 단계씩 파괴 (랜드마크 제외)")

    def use(self, game: 'Game'):
        return LandResult(
            message=f"지진을 발생시킬 도시 번호를 입력하세요",
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

        # 건물 단계 1단계 하락
        current_level = target_city.get_building().get_level()
        if current_level > 1:
            target_city.get_building()._level = current_level - 1

        return LandResult(
            message=f"{target_city.get_name()}의 건물 레벨이 1단계 하락되었습니다.",
            actions=["확인"]
        )
