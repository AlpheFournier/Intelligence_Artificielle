from Common.base_player import BasePlayer
import random

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
        beasts = self.grid.get_beasts(self.player_name.lower()) # [(x, y, #)]
        new_beasts = []

        if beasts[0][0] == 0:
            if beasts[0][1] == 0:
                random_fool_number = random.choice([5,7,8])
            elif beasts[0][1] == (self.grid.size_n - 1):
                random_fool_number = random.choice([2,3,5])
            else:
                random_fool_number = random.choice([2,3,5,7,8])  
        elif beasts[0][0] == (self.grid.size_m - 1):
            if beasts[0][1] == 0:
                random_fool_number = random.choice([4,6,7])
            elif beasts[0][1] == (self.grid.size_n - 1):    
                random_fool_number = random.choice([1,2,4])
            else:
                random_fool_number = random.choice([1,2,4,6,7]) 
        elif beasts[0][1] == 0:
            random_fool_number = random.choice([4,5,6,7,8])
        elif beasts[0][1] == (self.grid.size_n - 1):
            random_fool_number = random.choice([1,2,3,4,5])
        else:                              
            random_fool_number = random.randint(1,8)

        if random_fool_number == 1:
            self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] - 1, beasts[0][1] - 1, self.player_name, beasts[0][2])
            new_beasts.append((beasts[0][0] - 1, beasts[0][1] - 1))
        if random_fool_number == 2:
            self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0], beasts[0][1] - 1, self.player_name, beasts[0][2])
            new_beasts.append((beasts[0][0], beasts[0][1] - 1))
        if random_fool_number == 3:
            self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] + 1, beasts[0][1] - 1, self.player_name, beasts[0][2])
            new_beasts.append((beasts[0][0] + 1, beasts[0][1] - 1))
        if random_fool_number == 4:
            self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] - 1, beasts[0][1], self.player_name, beasts[0][2])
            new_beasts.append((beasts[0][0] - 1, beasts[0][1]))
        if random_fool_number == 5:
            self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] + 1, beasts[0][1], self.player_name, beasts[0][2])
            new_beasts.append((beasts[0][0] + 1, beasts[0][1]))
        if random_fool_number == 6:
            self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] - 1, beasts[0][1] + 1, self.player_name, beasts[0][2])
            new_beasts.append((beasts[0][0] - 1, beasts[0][1] + 1))
        if random_fool_number == 7:
            self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0], beasts[0][1] + 1, self.player_name, beasts[0][2])
            new_beasts.append((beasts[0][0], beasts[0][1] + 1))
        if random_fool_number == 8:
            self.grid.move_entities(beasts[0][0], beasts[0][1], beasts[0][0] + 1, beasts[0][1] + 1, self.player_name, beasts[0][2])
            new_beasts.append((beasts[0][0] + 1, beasts[0][1] + 1))                        

        return (beasts, new_beasts)
