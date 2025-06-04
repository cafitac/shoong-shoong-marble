from app.board_space.abstract import BoardSpace, SpaceColor
from app.board_space.property.impl import PropertySpace
from app.board_space.tourist_spot.impl import TouristSpotSpace
from app.board_space.start.impl import StartSpace
from app.board_space.bonus_game.impl import BonusGameSpace
from app.board_space.chance.impl import ChanceSpace
from app.board_space.island.impl import IslandSpace
from app.board_space.olympic.impl import OlympicSpace
from app.board_space.tour.impl import TourSpace
from app.board_space.tax_office.impl import TaxOfficeSpace
from app.money.impl import Money
from typing import List


class Board:
    def __init__(self, spaces: List[BoardSpace]):
        self._spaces = spaces

    @classmethod
    def create_from_data(cls, spaces_data: List[dict]) -> 'Board':
        cleaned_spaces = []
        for data in spaces_data:
            cleaned_data = {}
            # BOM 문자 처리
            for key, value in data.items():
                cleaned_key = key.replace('\ufeff', '')  # BOM 문자 제거
                cleaned_data[cleaned_key] = value
            cleaned_spaces.append(cleaned_data)

        spaces = [cls._create_space(data) for data in cleaned_spaces]
        return cls(spaces)

    @staticmethod
    def _create_space(data: dict) -> BoardSpace:
        print(data)
        seq = int(data['seq'])
        space_type = data['type']
        color = SpaceColor[data['color']] if data['color'] != 'None' else SpaceColor.NONE
        price = int(data['price']) if data['price'] != 'None' else None
        name = data['name']

        if space_type == 'property':
            return PropertySpace(seq=seq, color=color, price=Money(price), name=name)
        elif space_type == 'tourist_spot':
            return TouristSpotSpace(seq=seq, price=Money(price), name=name)
        elif space_type == 'start':
            return StartSpace(seq=seq, name=name)
        elif space_type == 'bonus_game':
            return BonusGameSpace(seq=seq, name=name)
        elif space_type == 'chance_card':
            return ChanceSpace(seq=seq, name=name)
        elif space_type == 'island':
            return IslandSpace(seq=seq, name=name)
        elif space_type == 'olympic':
            return OlympicSpace(seq=seq, name=name)
        elif space_type == 'tour':
            return TourSpace(seq=seq, name=name)
        elif space_type == 'tax_office':
            return TaxOfficeSpace(seq=seq, name=name, board_spaces=[])
        else:
            raise ValueError(f"알 수 없는 공간 유형: {space_type}")

    def get_spaces(self) -> List[BoardSpace]:
        return self._spaces

    def get_space(self, index: int) -> BoardSpace:
        return self._spaces[index]

    def get_space_count(self) -> int:
        return len(self._spaces)
