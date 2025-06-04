from app.board_space.abstract import BoardSpace
from app.player.impl import Player
from app.board_space.property.impl import PropertySpace

class StartSpace(BoardSpace):

    def on_land(self, player: Player):
        print(f"{player}님이 출발지에 도착했습니다. 자신의 땅 중 원하는 지역 하나를 골라 건물을 지을 수 있습니다.")
        
        # 1. 플레이어가 소유한 땅 목록 찾기
        owned_properties = [
            space for space in getattr(player, "board_spaces", [])
            if isinstance(space, PropertySpace) and space._owner == player
        ]
        if not owned_properties:
            print("소유한 땅이 없습니다.")
            return

        # 2. 업그레이드 가능한 땅 목록 출력
        upgradable = []
        for idx, prop in enumerate(owned_properties):
            building = prop._building
            level = building.get_level()
            name = getattr(prop, "_name", f"땅{idx+1}")
            if building.can_build_landmark():
                upgradable.append((idx, prop, "랜드마크"))
                print(f"{idx}: {name} (호텔 → 랜드마크 업그레이드 가능)")
            elif level < 3:
                upgradable.append((idx, prop, "업그레이드"))
                print(f"{idx}: {name} (현재 레벨: {level}, 업그레이드 가능)")

        if not upgradable:
            print("업그레이드 가능한 땅이 없습니다.")
            return

        # 3. 플레이어가 원하는 땅 선택
        try:
            choice = int(input("업그레이드할 땅 번호를 선택하세요: "))
            _, selected_prop, upgrade_type = next(item for item in upgradable if item[0] == choice)
        except (ValueError, StopIteration):
            print("잘못된 선택입니다.")
            return

        building = selected_prop._building
        cost = building.get_upgrade_cost()
        if player.get_cash() < cost:
            print("현금이 부족합니다.")
            return

        player.spend(cost)
        building.upgrade()
        if upgrade_type == "랜드마크":
            print(f"{selected_prop._name}에 랜드마크를 건설했습니다!")
        else:
            print(f"{selected_prop._name}의 건물을 업그레이드했습니다!")
