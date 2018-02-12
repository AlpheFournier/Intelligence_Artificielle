from Common.base_player import BasePlayer

class Player(BasePlayer):
    def __init__(self, **kwargs):
        """
        Available vars:
        player_name = The name
        grid = The grid as a Grid object
        current_turn = The current turn
        """
        super(Player, self).__init__(**kwargs)

    def get_next_moves(self):
        """ Override the next move """
        humans = self.grid.get_humans(self.homes) # [(x1, y1, n1), (...)]
        beasts = self.grid.get_beasts(self.player_name.lower()) # [(x, y, #)]
        new_beasts = []

        if len(humans) != 0:
            for index, human in enumerate(humans):
                distance = (beasts[0][0] - human[0])**2 + (beasts[0][1] - human[1])**2
                if index == 0:
                    min_distance = distance
                    min_index = index
                elif distance < min_distance:
                    min_distance = distance
                    min_index = index

            closest_other_specie = humans[min_index]

        else:
            enemies = self.grid.get_beasts(self.enemy_name.lower())
            for index, enemy in enumerate(enemies):
                distance = (beasts[0][0] - enemy[0])**2 + (beasts[0][1] - enemy[1])**2
                if index == 0:
                    min_distance = distance
                    min_index = index
                elif distance < min_distance:
                    min_distance = distance
                    min_index = index

            closest_other_specie = enemies[min_index]

        # Choose the direction
        if closest_other_specie[1] == beasts[0][1]: # On est sur la même ligne
            if closest_other_specie[0] > beasts[0][0]: # On va à droite
                self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] + 1, beasts[0][1], self.player_name, beasts[0][2])
                new_beasts.append((beasts[0][0] + 1, beasts[0][1]))
            else: # On va à gauche
                self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] - 1, beasts[0][1], self.player_name, beasts[0][2])
                new_beasts.append((beasts[0][0] - 1, beasts[0][1]))

        elif closest_other_specie[0] == beasts[0][0]: # On est sur la même colonne
            if closest_other_specie[1] < beasts[0][1]: # On va en haut
                self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0], beasts[0][1] - 1, self.player_name, beasts[0][2])
                new_beasts.append((beasts[0][0], beasts[0][1] - 1))
            else: # On va en bas
                self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0], beasts[0][1] + 1, self.player_name, beasts[0][2])
                new_beasts.append((beasts[0][0], beasts[0][1] + 1))

        else: # On est en diagonale
            if closest_other_specie[0] > beasts[0][0] and closest_other_specie[1] < beasts[0][1]: # En haut à droite
                self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] + 1, beasts[0][1] - 1, self.player_name, beasts[0][2])
                new_beasts.append((beasts[0][0] + 1, beasts[0][1] - 1))
            elif closest_other_specie[0] < beasts[0][0] and closest_other_specie[1] < beasts[0][1]: # En haut à gauche
                self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] - 1, beasts[0][1] - 1, self.player_name, beasts[0][2])
                new_beasts.append((beasts[0][0] - 1, beasts[0][1] - 1))
            elif closest_other_specie[0] > beasts[0][0] and closest_other_specie[1] > beasts[0][1]: # En bas à droite
                self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] + 1, beasts[0][1] + 1, self.player_name, beasts[0][2])
                new_beasts.append((beasts[0][0] + 1, beasts[0][1] + 1))
            elif closest_other_specie[0] < beasts[0][0] and closest_other_specie[1] > beasts[0][1]: # En bas à gauche
                self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] - 1, beasts[0][1] + 1, self.player_name, beasts[0][2])
                new_beasts.append((beasts[0][0] - 1, beasts[0][1] + 1))
            else:
                print("ERROR IN PATHFINDING")

        return (beasts, new_beasts)
