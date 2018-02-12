""" Basic implementation of a grid """
from copy import copy
class Grid():
    """ A grid """
    def __init__(self, n, m):
        self.__size_n = n
        self.__size_m = m
        self.__grid = [[{
            "humans": 0,
            "vampires": 0,
            "werewolves": 0
        } for y in range(n)] for x in range(m)]
        self.__previous_grid = None

    @property
    def size_n(self):
        return self.__size_n

    @property
    def size_m(self):
        return self.__size_m

    @property
    def previous_grid(self):
        return self.__previous_grid    

    @staticmethod
    def get_str(dic):
        """ Change a dict into a string representation for printing """
        if dic["humans"] != 0:
            return "[{}H]".format(dic["humans"])
        elif dic["vampires"] != 0:
            return "[{}V]".format(dic["vampires"])
        elif dic["werewolves"] != 0:
            return "[{}W]".format(dic["werewolves"])
        else:
            return "[XX]" 

    def __repr__(self):
        grid_to_print = []
        for y in range(self.__size_n):
            ligne = []
            for x in range(self.__size_m):
                ligne.append(self.get_str(self.__grid[x][y]))
            grid_to_print.append(ligne)
        return ('\n'.join(''.join(map(str,l)) for l in grid_to_print))

    def update_grid(self, commands):
        """ Read a command list and update the grid accordingly """
        for command in list(commands):
            self.__grid[command[0]][command[1]] = {
                "humans": command[2],
                "vampires": command[3],
                "werewolves": command[4]
            }
        # We need to explicitely shallow copy the dictionnaries for them not to update!
        self.__previous_grid = [[copy(self.grid[x][y]) for y in range(self.__size_n)] for x in range(self.__size_m)]

    def get_humans(self, homes):
        """ List the humans on the grid """
        humans = [
            (i, j, self.__grid[i][j]["humans"]) \
                for (i, j) in homes \
                if self.__grid[i][j]["humans"] != 0
        ]
        
        return humans

    def get_beasts(self, name):
        """ List the beasts on the grid """
        beasts = [
            (i, j, self.__grid[i][j][name]) \
                for i, col in enumerate(self.__grid) \
                for j, slot in enumerate(col) \
                if self.__grid[i][j][name] != 0
        ]

        return beasts

    def move_entities(self, x1, y1, x2, y2, name, amount):
        """ Move the entities from the first slot to the other """
        print("[GRID - {}] Moving entities from {}-{} to {}-{}".format(name, x1, y1, x2, y2))
        name = name.lower()
        # 1. Read the current amount
        current_amount = self.__grid[x1][y1][name]
        if current_amount < amount:
            print("[GRID - {}] Can't apply this move, amount is more than current".format(name))
            print("[GRID - {}] Moving the total instead: {}".format(name, current_amount))
            amount = current_amount
        
        # 2. Remove the entities
        self.__grid[x1][y1][name] = current_amount - amount

        # 3. Add the entities to the other spot
        self.__grid[x2][y2][name] += amount

    @property
    def grid(self):
        """ Getter for the grid """
        return self.__grid
