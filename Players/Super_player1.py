from Common.base_player import BasePlayer
from copy import copy
from Common.grid import Grid
from random import randint


class Player(BasePlayer):
    def __init__(self, **kwargs):
        """
        Available vars:
        player_name = The name
        grid = The grid as a Grid object
        current_turn = The current turn
        """
        super(Player, self).__init__(**kwargs)

    def copy_grid(self):
        previous_grid = Grid(self.grid.size_n, self.grid.size_m)
        for i in range(self.grid.size_n):
            for j in range(self.grid.size_m):
                previous_grid.grid[j][i] = copy(self.grid.grid[j][i])
        return previous_grid

    def cost_function(self):
        moves = self.get_available_moves()
        beasts = self.grid.get_beasts(self.player_name.lower())
        where_to_go = [] #liste de tuple position
        i = 0 # se déplace dans la liste moves
        for move in moves:
            best_score = [move[0], 0] #initialisation
            costs = []
            for position in move:
                current_cost = 0
                x, y = position
                E = self.grid.grid[x][y][self.enemy_name.lower()]
                H = self.grid.grid[x][y]['humans']
                U = beasts[i][2]
                if 0 < E:
                    current_cost = U - E/1.5
                    costs += [(E, current_cost)]
                elif 0 < H:
                    current_cost = U - H
                    costs += [(H, current_cost)]
                else:
                    costs += [0, 0]
                if current_cost >= best_score[1]:
                    best_score = [position, current_cost]
            if best_score[1] == 0:
                rand = randint(0, len(move)-1)
                where_to_go += [move[rand]]
            else:
                where_to_go += [best_score[0]]
            i += 1
        return where_to_go


    def get_next_moves(self):
        """ Override the next move """
        where_to_go = self.cost_function()
        #humans = self.grid.get_humans(self.homes) # [(x1, y1, n1), (...)]
        beasts = self.grid.get_beasts(self.player_name.lower()) # [(x, y, #)]
        new_beasts = [] #liste de tuple
        for i in range(len(where_to_go)):
            position_to_go = where_to_go[i]
            self.grid.move_entities(beasts[i][0], beasts[i][1], position_to_go[0], position_to_go[1], self.player_name, beasts[i][2])
            new_beasts.append(position_to_go)


        return (beasts, new_beasts)
