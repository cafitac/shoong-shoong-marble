import csv
from pathlib import Path


def get_board_space_data() -> list:
    spaces_data = []

    script_path = Path(__file__).resolve()
    script_dir = script_path.parent.parent

    csv_path = script_dir / 'static/board_space_data.csv'
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        spaces_data = list(csv_reader)

    return spaces_data
