import random
from typing import List
from typing import Tuple

import pygame
from boardgame.hexgrid import init_hexgrid
from boardgame.hexgrid import render_hexgrid
from boardgame.hexagon import create_hexagon
from boardgame.players import create_player
from boardgame.armies import create_army
from boardgame.global_utils import get_random_colour
from boardgame.combat import determine_combat_result

# pylint: disable=no-member


def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    hexgrid = init_hexgrid(num_x=3, num_y=3, leftmost_position=(50,50), flat_top=True)
    # print(len(hexgrid))
    # print(hexgrid)

    num_players = 2
    players = []
    for p in range(num_players):
        players.append(create_player(p, colour=get_random_colour()))

    # initialise player's armies
    for p in range(len(players)):
        init_army = create_army(players[p])
        init_hex = hexgrid[int(round(p/len(players) - 1))]
        init_hex.add_army(init_army)
    
    phase_of_play = "marching"
    marching_army_hex = create_hexagon((0,0))

    terminated = False
    while not terminated:
        
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                match phase_of_play:
                    case "marching":
                        click_pos = event.pos

                        clicked_hex = [
                            hexagon for hexagon in hexgrid if hexagon.collide_with_point(click_pos)
                        ]

                        if len(clicked_hex):
                            clicked_hex = clicked_hex[0]

                            # select marching army
                            if (marching_army_hex.army is None) and (clicked_hex.army is not None):
                                marching_army_hex = clicked_hex
                                for neighbour in marching_army_hex.compute_neighbours(hexgrid):
                                    neighbour.update_border_colour(colour=marching_army_hex.army.colour)
                            
                            # move marching army to vacant hex
                            elif (marching_army_hex.army is not None) and (clicked_hex.army is None):
                                if clicked_hex in marching_army_hex.compute_neighbours(hexgrid):
                                    for neighbour in marching_army_hex.compute_neighbours(hexgrid):
                                        neighbour.update_border_colour()
                                    clicked_hex.add_army(marching_army_hex.army)
                                    marching_army_hex.remove_army()

                            # initiate combat
                            elif (
                                (marching_army_hex.army is not None) and 
                                (clicked_hex.army is not None) and 
                                (clicked_hex.army.player != marching_army_hex.army.player)
                            ):
                                for neighbour in marching_army_hex.compute_neighbours(hexgrid):
                                    neighbour.update_border_colour()
                                
                                combat_result = determine_combat_result(marching_army_hex, clicked_hex, hexgrid, screen)

                                # match combat_result:
                                #     case "attack_wins":
                                        
                                #     case "defense_wins":
                                        

            if event.type == pygame.QUIT:
                terminated = True

        

        render_hexgrid(screen, hexgrid)
        for hexagon in hexgrid:
            hexagon.update()
        
        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()