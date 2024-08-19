
from typing import List
from typing import Tuple

import pygame
import boardgame.globals as bg
from boardgame.hexagon import HexagonTile
from boardgame.hexagon import create_hexagon
from boardgame.hexagon import get_random_hex_type

def init_hexgrid(num_x=20, num_y=20, leftmost_position=(-50,-50), flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    leftmost_hexagon = create_hexagon(position=leftmost_position, flat_top=flat_top, hex_type=get_random_hex_type())
    # leftmost_hexagon.add_army(create_army())
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x % 2 == 1 or flat_top else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top, hex_type=get_random_hex_type())
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        for i in range(num_x):
            if i:
                x, y = hexagon.position  # type: ignore
                if flat_top:
                    if i % 2 == 1:
                        position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                    else:
                        position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
                else:
                    position = (x + hexagon.minimal_radius * 2, y)
                hexagon = create_hexagon(position, flat_top=flat_top, hex_type=get_random_hex_type())
                hexagons.append(hexagon)

    return hexagons


def render_hexgrid(screen, hexagons):
    """Renders hexagons on the screen"""
    # screen.fill((0, 0, 0))
    for hexagon in hexagons:
        hexagon.render(screen)

    # draw borders around colliding hexagons and neighbours
    mouse_pos = pygame.mouse.get_pos()
    colliding_hexagons = [
        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    ]
    for hexagon in colliding_hexagons:
        # for neighbour in hexagon.compute_neighbours(hexagons):
        #     neighbour.render_highlight(screen, border_colour=(100, 100, 100))
        hexagon.render_highlight(screen, border_colour=(0, 0, 0))
    pygame.display.flip()