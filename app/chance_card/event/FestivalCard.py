from app.board_space.land_result import LandResult
from app.board_space.property.impl import PropertySpace
from app.chance_card.abstract import ChanceCard, ChanceCardType
from typing import TYPE_CHECKING

from app.player.impl import Player

if TYPE_CHECKING:
    from app.game.impl import Game

# 축제(올림픽) 개최
# 내 현재 도시에 올림픽 마크 설치 → 해당 통행료 ×2 (중첩 불가)
class FestivalCard(ChanceCard):
    def __init__(self):
        super().__init__(ChanceCardType.INSTANT, "축제 개최", "즉시 내 현재 도시에 축제 마크 설치 > 해당 통행료 x 2 (중첩 불가)")

    def use(self, game: 'Game'):
        player = game.get_turn_manager().get_prev_player()  # 현재 플레이어

        # 1. 플레이어가 소유한 도시 목록 찾기
        owned_properties = [
            space for space in getattr(self, "_board_spaces", [])
            if isinstance(space, PropertySpace) and space._owner == player
        ]
        if not owned_properties:
            return LandResult(
                message="소유한 도시가 없습니다.",
                actions=["확인"]
            )

        # 2. 도시 목록 출력
        city_list = ""
        for idx, prop in enumerate(owned_properties):
            name = getattr(prop, "_name", f"도시{idx + 1}")
            print(f"{idx}: {name}")
            city_list += f"{idx}: {name}\n"

        # 3. 플레이어가 올림픽 개최 도시 선택
        return LandResult(
            message=f"올림픽을 개최할 도시 번호를 입력하세요:\n{city_list}",
            actions=["확인"],
            callback=lambda input_text: self._handle_city_selection(player, input_text, owned_properties),
            is_prompt=True
        )

    def _handle_city_selection(self, player: Player, input_text: str, properties: list[PropertySpace]):
        try:
            idx = int(input_text.strip())
            selected_prop = properties[idx]
        except (ValueError, IndexError):
            city_list = ""
            for idx, prop in enumerate(properties):
                name = getattr(prop, "_name", f"도시{idx + 1}")
                print(f"{idx}: {name}")
                city_list += f"{idx}: {name}\n"
            return LandResult(
                message=f"잘못된 입력입니다.\n올림픽을 개최할 도시 번호를 입력하세요:\n{city_list}",
                actions=["확인"],
                callback=lambda input_text1: self._handle_city_selection(player, input_text1, properties),
                is_prompt=True
            )

        # 기존 올림픽 도시 플래그 해제 (전체 board_spaces에서)
        for space in getattr(player, "board_spaces", []):
            if isinstance(space, PropertySpace):
                space._is_festival = False

        # 선택한 도시에 올림픽 플래그 설정
        selected_prop._is_festival = True

        return LandResult(
            message=f"{getattr(selected_prop, '_name', '도시')}에서 올림픽이 개최되었습니다! 통행료가 2배로 증가합니다.",
            actions=["확인"]
        )
