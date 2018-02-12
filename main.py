""" Main execution module """
from Players import random_fool, go_to_humans, Super_player1

HOST = "localhost"
PORT = "5555"

def run():
    """ Main function """
    player_1 = random_fool.Player(host=HOST, port=PORT)
    player_2 = go_to_humans.Player(host=HOST, port=PORT)
    player_1.start()
    player_2.start()

if __name__ == "__main__":
    run()
