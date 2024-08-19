from dataclasses import dataclass
from typing import List
from typing import Tuple

import boardgame.globals as bg
# from boardgame.armies import Army

@dataclass
class Player:

    id: int
    colour: str
        
    def __post_init__(self):
        self.name = "Player " + str(self.id + 1)
        self.units_in_reserve = bg.AVAILABLE_UNITS
        self.resources = bg.STARTTING_RESOURCES
        self.armies = []

    def add_army(self, army):
        self.armies.append(army)

def create_player(id, colour):
    return Player(id, colour)