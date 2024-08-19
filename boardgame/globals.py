HEX_TYPE_TO_COLOR_MAP = {
    "water": (30,129,176),
    "forest": (139, 69, 19),
    "hill": (226,135,67),
    "pasture": (107,145,35),
    "field": (248,202,140),
    "mountain": (128, 128, 128),
    "desert": (238,238,228)
}

UNIT_ATTACK_STRENGTH = {
    "infantry": 1,
    "knight": 1,
    "archer": 1,
}

UNIT_DEFENSE_STRENGTH = {
    "infantry": 1,
    "knight": 1,
    "archer": 0,
}

UNIT_SUPPORT_STRENGTH = {
    "infantry": 0,
    "knight": 0,
    "archer": 1,
}

UNIT_SHAPES = {
    "infantry": "circle",
    "knight": "square",
    "archer": "triangle",
}

UNIT_MOVEMENT_POINTS = {
    "infantry": 2,
    "knight": 3,
    "archer": 2,
}

AVAILABLE_UNITS = {
    "infantry": 6,
    "knight": 3,
    "archer": 3,
}

MAX_UNITS_PER_ARMY = 3
UNIT_SIZE = 200

STARTTING_RESOURCES = {
    "food": 1,
    "wood": 1,
    "brick": 1,
    "horses": 1,
    "iron": 1
}

BORDER_HIGHLIGHT_THICKNESS = 4