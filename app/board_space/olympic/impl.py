from app.board_space.abstract import BoardSpace
from app.player.impl import Player
from app.board_space.property.impl import PropertySpace

class OlympicSpace(BoardSpace):

    def on_land(self, player: Player):
        print(f"{player}님이 올림픽 지역에 도착했습니다. 자신이 소유한 도시 중 한 곳을 선택해 올림픽을 개최할 수 있습니다.")
        print("올림픽 개최 시, 올림픽이 개최돈 도시의 통행료가 2배로 증가합니다.")

        # 1. 플레이어가 소유한 도시 목록 찾기
        owned_properties = [
            space for space in getattr(player, "board_spaces", [])
            if isinstance(space, PropertySpace) and space._owner == player
        ]
        if not owned_properties:
            print("소유한 도시가 없습니다.")
            return

        # 2. 도시 목록 출력
        for idx, prop in enumerate(owned_properties):
            name = getattr(prop, "_name", f"도시{idx+1}")
            print(f"{idx}: {name}")

        # 3. 플레이어가 올림픽 개최 도시 선택
        try:
            choice = int(input("올림픽을 개최할 도시 번호를 선택하세요: "))
            selected_prop = owned_properties[choice]
        except (ValueError, IndexError):
            print("잘못된 선택입니다.")
            return

        # 4. 기존 올림픽 도시 플래그 해제 (전체 board_spaces에서)
        for space in getattr(player, "board_spaces", []):
            if isinstance(space, PropertySpace):
                space.olympic = False

        # 5. 선택한 도시에 올림픽 플래그 설정
        selected_prop.olympic = True
        print(f"{getattr(selected_prop, '_name', '도시')}에서 올림픽이 개최되었습니다! 통행료가 2배로 증가합니다.")
