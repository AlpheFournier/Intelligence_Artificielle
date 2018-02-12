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
        pass
