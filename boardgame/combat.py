import random
import pygame

from boardgame.hexagon import HexagonTile
from boardgame.global_utils import create_dice_image

def determine_combat_result(attacking_army_hex: HexagonTile, defending_army_hex: HexagonTile, hexgrid, screen):
    attacking_army = attacking_army_hex.army
    attacking_player = attacking_army.player
    defending_army = defending_army_hex.army
    defending_player = defending_army.player

    attacking_strength = attacking_army.army_attack_strength
    defending_strength = defending_army.army_defense_strength

    # print(attacking_strength)
    # print(defending_strength)

    neighbouring_hexes = defending_army_hex.compute_neighbours(hexgrid)
    support_hexes = [h for h in neighbouring_hexes if h != attacking_army_hex]
    support_armies = [h.army for h in support_hexes if h.army is not None]

    attacking_support_armies = [a for a in support_armies if a.player == attacking_player]
    attacking_support_strength = 0
    for a in attacking_support_armies:
        attacking_support_strength += a.army_support_strength

    defending_support_armies = [a for a in support_armies if a.player == defending_player]
    defending_support_strength = 0
    for a in defending_support_armies:
        defending_support_strength += a.army_support_strength

    # print(attacking_support_strength)
    # print(defending_support_strength)

    final_attack_strength = attacking_strength + attacking_support_strength
    final_defense_strength = defending_strength + defending_support_strength

    # print(final_attack_strength)
    # print(final_defense_strength)

    if final_attack_strength > final_defense_strength:
        result = "attack_wins"
    elif final_attack_strength < final_defense_strength:
        result = "defense_wins"
    elif final_attack_strength == final_defense_strength:
        dot_color = (0, 0, 0)  # Black

        attacking_dice_value = random.randint(1, 6)
        defending_dice_value = random.randint(1, 6)

        attacking_dice_image = create_dice_image(100, attacking_player.colour, dot_color, attacking_dice_value)
        defending_dice_image = create_dice_image(100, defending_player.colour, dot_color, defending_dice_value)
        
        print(attacking_dice_value)
        print(defending_dice_value)

        screen.blit(attacking_dice_image, (850,100))
        screen.blit(defending_dice_image, (850,200))

        if attacking_dice_value >= defending_dice_value:
            result = "attack_wins"
        else:
            result = "defense_wins"

        pygame.display.update()

    print(result)
    return result
