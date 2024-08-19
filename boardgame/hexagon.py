# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 14:07:18 2022

@author: richa
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List
from typing import Tuple

import pygame
import boardgame.globals as bg
from boardgame.armies import Army
from boardgame.global_utils import get_hexagon_coords


@dataclass
class HexagonTile:
    """Hexagon class"""

    radius: float
    position: Tuple[float, float]
    hex_type: str
    army: Army = None
    colour: Tuple[int, ...] = None
    highlight_offset: int = 3
    max_highlight_ticks: int = 15

    def __post_init__(self):
        self.vertices = self.compute_vertices()
        self.border_highlight_vertices = self.compute_border_highlight_vertices()
        self.highlight_tick = 0
        self.colour = bg.HEX_TYPE_TO_COLOR_MAP[self.hex_type]
        self.border_colour = bg.HEX_TYPE_TO_COLOR_MAP[self.hex_type]

    def update(self):
        """Updates tile highlights"""
        if self.highlight_tick > 0:
            self.highlight_tick -= 1

    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - minimal_radius, y + half_radius),
            (x - minimal_radius, y + 3 * half_radius),
            (x, y + 2 * self.radius),
            (x + minimal_radius, y + 3 * half_radius),
            (x + minimal_radius, y + half_radius),
        ]
    
    def compute_border_highlight_vertices(self, border_offset=bg.BORDER_HIGHLIGHT_THICKNESS) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y - border_offset),
            (x - minimal_radius, y + half_radius - border_offset),
            (x - minimal_radius, y + 3 * half_radius + border_offset),
            (x, y + 2 * self.radius + border_offset),
            (x + minimal_radius, y + 3 * half_radius + border_offset),
            (x + minimal_radius, y + half_radius - border_offset),
        ]

    def compute_neighbours(self, hexagons: List[HexagonTile]) -> List[HexagonTile]:
        """Returns hexagons whose centres are two minimal radiuses away from self.centre"""
        # could cache results for performance
        return [hexagon for hexagon in hexagons if self.is_neighbour(hexagon)]

    def collide_with_point(self, point: Tuple[float, float]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return math.dist(point, self.centre) < self.minimal_radius

    def is_neighbour(self, hexagon: HexagonTile) -> bool:
        """Returns True if hexagon centre is approximately
        2 minimal radiuses away from own centre
        """
        distance = math.dist(hexagon.centre, self.centre)
        return math.isclose(distance, 2 * self.minimal_radius, rel_tol=0.05)

    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, self.highlight_colour, self.vertices)
        # pygame.draw.lines(screen, self.border_colour, True, self.border_highlight_vertices, bg.BORDER_HIGHLIGHT_THICKNESS)
        pygame.draw.aalines(screen, self.border_colour, closed=True, points=self.border_highlight_vertices)

        if self.army:
            self.army.draw_army(screen, self.centre)
            

    def render_highlight(self, screen, border_colour) -> None:
        """Draws a border around the hexagon with the specified colour"""
        self.highlight_tick = self.max_highlight_ticks
        # pygame.draw.polygon(screen, self.highlight_colour, self.vertices)
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    def update_colour(self, colour) -> None:
        self.colour = colour

    def update_border_colour(self, colour=None):
        if colour is None:
            colour = self.colour
        self.border_colour = colour
        

    def add_army(self, army: Army):
        self.army = army

    def remove_army(self):
        self.army = None

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return (x, y + self.radius)

    @property
    def minimal_radius(self) -> float:
        """Horizontal length of the hexagon"""
        # https://en.wikipedia.org/wiki/Hexagon#Parameters
        return self.radius * math.cos(math.radians(30))

    @property
    def highlight_colour(self) -> Tuple[int, ...]:
        """Colour of the hexagon tile when rendering highlight"""
        offset = self.highlight_offset * self.highlight_tick
        brighten = lambda x, y: x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.colour)


class FlatTopHexagonTile(HexagonTile):
    def compute_vertices(self) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x, y),
            (x - half_radius, y + minimal_radius),
            (x, y + 2 * minimal_radius),
            (x + self.radius, y + 2 * minimal_radius),
            (x + 3 * half_radius, y + minimal_radius),
            (x + self.radius, y),
        ]
    
    def compute_border_highlight_vertices(self, border_offset=bg.BORDER_HIGHLIGHT_THICKNESS) -> List[Tuple[float, float]]:
        """Returns a list of the hexagon's vertices as x, y tuples"""
        # pylint: disable=invalid-name
        return get_hexagon_coords(self.centre, self.radius - border_offset)

    @property
    def centre(self) -> Tuple[float, float]:
        """Centre of the hexagon"""
        x, y = self.position  # pylint: disable=invalid-name
        return (x + self.radius / 2, y + self.minimal_radius)
    
def create_hexagon(position, radius=50, flat_top=False, hex_type="water") -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(radius, position, hex_type)

def get_random_hex_type():
    return random.choice(list(bg.HEX_TYPE_TO_COLOR_MAP.keys()))