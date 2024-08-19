from dataclasses import dataclass
from typing import List
from typing import Tuple
import pygame
import math

import boardgame.globals as bg
from boardgame.global_utils import get_equilateral_triangle_coords, get_square_coords
from boardgame.players import Player


@dataclass
class MilitaryUnit:
    """Military unit class"""

    unit_type: str
    routed: bool = False

    def __post_init__(self):
        self.attack_strength = bg.UNIT_ATTACK_STRENGTH[self.unit_type]
        self.defense_strength = bg.UNIT_DEFENSE_STRENGTH[self.unit_type]
        self.support_strength = bg.UNIT_SUPPORT_STRENGTH[self.unit_type]
        self.shape = bg.UNIT_SHAPES[self.unit_type]
        self.movement_points = bg.UNIT_MOVEMENT_POINTS[self.unit_type]

    def draw_unit(self, screen, colour, centre, size = bg.UNIT_SIZE):
        match self.shape:
            case "circle":
                pygame.draw.circle(screen, colour, centre, math.sqrt(size / math.pi))
            case "triangle":
                pygame.draw.polygon(screen, colour, get_equilateral_triangle_coords(centre, size))
            case "square":
                pygame.draw.rect(screen, colour, pygame.Rect(get_square_coords(centre, size)))



@dataclass
class Army:
    """Class for a collection of units"""
    
    player: Player
    units: List[MilitaryUnit]
    
    def __post_init__(self):
        self.colour = self.player.colour

    @property
    def num_units(self):
        return len(self.units)
    
    @property
    def army_attack_strength(self):
        army_attack_strength = 0
        for unit in self.units:
            army_attack_strength += unit.attack_strength
        return army_attack_strength

    @property
    def army_defense_strength(self):
        army_defense_strength = 0
        for unit in self.units:
            army_defense_strength += unit.defense_strength
        return army_defense_strength

    @property
    def army_support_strength(self):
        army_support_strength = 0
        for unit in self.units:
            army_support_strength += unit.support_strength
        return army_support_strength

    @property
    def army_movement_points(self):
        army_movement_points = math.inf
        for unit in self.units:
            army_movement_points = min(unit.movement_points, army_movement_points)
        return army_movement_points

    def draw_army(self, screen, army_centre):
        if self.num_units == 1:
            self.units[0].draw_unit(screen, self.colour, army_centre)

        elif self.num_units == 2:
            for u in range(self.num_units):
                centre = (army_centre[0] - 15 + u*30, army_centre[1])
                self.units[u].draw_unit(screen, self.colour, centre)
        elif self.num_units == 3:
            for u in range(self.num_units):
                if u == 0:
                    centre = (army_centre[0] - 15, army_centre[1] + 10)
                elif u == 1:
                    centre = (army_centre[0], army_centre[1] - 10)
                if u == 2:
                    centre = (army_centre[0] + 15, army_centre[1] + 10)

                self.units[u].draw_unit(screen, self.colour, centre)



def create_unit(unit_type = "infantry"):
    return MilitaryUnit(unit_type)

def create_army(player: Player, units = [create_unit("infantry"), create_unit("infantry"), create_unit("infantry")], ):
    army = Army(player, units)
    player.add_army(army)
    return army