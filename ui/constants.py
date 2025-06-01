# 색상 정의
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_SCREEN_BG = (100, 100, 100)
COLOR_BOARD_BG_UNROTATED = (143, 191, 143)
COLOR_CORNER_FILL = (234, 234, 234)
COLOR_MAIN_UPPER_BG = (200, 180, 168)
COLOR_MAIN_LOWER_BG = (220, 220, 220)
COLOR_PLAYER_PANEL_BG = (93, 95, 239)
COLOR_PLAYER_RANK_BG = (59, 50, 128)

# 폰트 설정
FONT_PATH_REGULAR = "assets/NanumGothic-Regular.ttf"
FONT_PATH_BOLD = "assets/NanumGothic-Bold.ttf"

# 게임 보드 설정 
BOARD_CELLS_PER_SIDE = 7
CELL_SHORT = 90
CELL_LONG = 138
CORNER_SIDE = CELL_LONG

ref_main_font_size = 18
ref_price_font_size = 16
ref_player_name_font_size = 22
ref_player_info_font_size = 20
ref_player_rank_font_size = 26
ref_corner_font_size = 28  # 코너 블록의 폰트 크기

sample_texts_pg = {"level": "{건물레벨}", "name": "{건물이름}", "price": "{가격}"}

# 보드 전체 크기 계산
BOARD_CONTENT_WIDTH = CORNER_SIDE + (BOARD_CELLS_PER_SIDE * CELL_SHORT) + CORNER_SIDE
BOARD_CONTENT_HEIGHT = CORNER_SIDE + (BOARD_CELLS_PER_SIDE * CELL_SHORT) + CORNER_SIDE

# 블록 색상
BLOCK_COLORS = {
    "upper_bg": COLOR_MAIN_UPPER_BG,
    "lower_bg": COLOR_MAIN_LOWER_BG,
    "text": COLOR_BLACK,
    "outline": COLOR_BLACK
}

# 보드 텍스트
BLOCK_TEXTS = {
    "level": "{건물레벨}",
    "name": "{건물이름}",
    "price": "{가격}"
}
# 보드 엣지 위치
BOARD_EDGES = {
    'top': 0,
    'bottom': BOARD_CONTENT_HEIGHT,
    'left': 0,
    'right': BOARD_CONTENT_WIDTH
}

# 코너 위치 계산
CORNER_POSITIONS = [
    (BOARD_EDGES['left'] + CORNER_SIDE / 2, BOARD_EDGES['bottom'] - CORNER_SIDE / 2),  # 좌하단
    (BOARD_EDGES['right'] - CORNER_SIDE / 2, BOARD_EDGES['bottom'] - CORNER_SIDE / 2),  # 우하단
    (BOARD_EDGES['left'] + CORNER_SIDE / 2, BOARD_EDGES['top'] + CORNER_SIDE / 2),  # 좌상단
    (BOARD_EDGES['right'] - CORNER_SIDE / 2, BOARD_EDGES['top'] + CORNER_SIDE / 2)  # 우상단
]

# 플레이어 색상
PLAYER_COLORS = [
    (255, 182, 182),  # 연한 빨강
    (182, 182, 255),  # 연한 파랑
    (182, 255, 182),  # 연한 초록
    (255, 255, 182),  # 연한 노랑
]
