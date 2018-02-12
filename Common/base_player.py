""" Base Player Class for every iteration """
from threading import Thread
import socket
import struct
from Common.grid import Grid

class BasePlayer(Thread):
    """ A player """
    def __init__(self, host, port):
        Thread.__init__(self)
        self.__host = host
        self.__port = port
        self.player_name = ""
        self.enemy_name = ""
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.__host, int(self.__port)))
        self.grid = None
        self.current_turn = 0
        self.__gameover = False
        self.__homes = []

    @property
    def gameover(self):
        return self.__gameover

    @property
    def homes(self):
        return self.__homes

    def __receive_data(self, size, fmt):
        data = bytes()
        while len(data) < size:
            data += self.__sock.recv(size - len(data))
        return struct.unpack(fmt, data)    

    @staticmethod
    def __grouper(_n, iterable):
        args = [iter(iterable)] * _n
        return zip(*args)

    def __initialize_game(self, nme=True):
        """ Runs the different checks and instanciate a map """
        print("[PLAYER - {}] Démarrage".format(self.player_name.capitalize()))
        if nme:
            # Envoi de la commande NME
            self.__sock.send("NME".encode("ascii"))
            self.__sock.send(struct.pack("1B", 6))
            self.__sock.send("Hummus".encode("ascii"))

        # SET
        header = self.__sock.recv(3).decode("ascii")
        if header != "SET":
            print("[PLAYER - {}] Protocol Error at SET".format(self.player_name.capitalize()))
        else:
            size_n, size_m = self.__receive_data(2, "2B")
            #print(size_n)
            #print(size_m)

        # HUM
        header = self.__sock.recv(3).decode("ascii")
        if header != "HUM":
            print("[PLAYER - {}] Protocol Error at HUM".format(self.player_name.capitalize()))
        else:
            number_of_homes = self.__receive_data(1, "1B")[0]
            homes_raw = self.__receive_data(
                number_of_homes * 2, "{}B".format(number_of_homes * 2)
            )
            self.__homes = list(self.__grouper(2, homes_raw))
            #print(homes)

        # HME
        header = self.__sock.recv(3).decode("ascii")
        if header != "HME":
            print("[PLAYER - {}] Protocol Error at HME".format(self.player_name.capitalize()))
        else:
            start_position = tuple(self.__receive_data(2, "2B"))
            #print(start_position)

        # MAP
        header = self.__sock.recv(3).decode("ascii")
        if header != "MAP":
            print("[PLAYER - {}] Protocol Error at MAP".format(self.player_name.capitalize()))
        else:
            number_map_commands = self.__receive_data(1, "1B")[0]
            map_commands_raw = self.__receive_data(
                number_map_commands * 5, "{}B".format(number_map_commands * 5)
            )
            map_commands = list(self.__grouper(5, map_commands_raw))
            #print(map_commands)
            for command in map_commands:
                if command[0] == start_position[0] and command[1] == start_position[1]:
                    if command[3] != 0:
                        self.player_name = "Vampires"
                        self.enemy_name = "Werewolves"
                    else:
                        self.player_name = "Werewolves"
                        self.enemy_name = "Vampires"

        # A ce stade, toutes les infos nécessaires sont disponibles
        print(
            "[PLAYER - {}] Received all the data. Initializing map".format(
                self.player_name.capitalize()
            )
        )

        self.grid = Grid(size_n, size_m)
        self.grid.update_grid(map_commands)
        print(self.grid)

    # def is_gameover(self):
    #     beasts = self.grid.get_beasts(self.player_name.lower())
    #     if len(beasts) == 0:
    #         return True
    #     else:
    #         return False

    def __reset_game(self):
        """ Resets the game to a blank map """
        self.grid = None

    def get_available_moves(self):
        """ Returns a list of neighbours represented as a list of tuples by group of beasts """
        beasts = self.grid.get_beasts(self.player_name.lower())
        n = self.grid.size_n #nb of lines
        m = self.grid.size_m #nb of columns
        new_neighbors = [[]]
        for i in range(len(beasts)):
            x = beasts[i][0]
            y = beasts[i][1]
            temp_neighbors = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
            for (k, l) in temp_neighbors:
                if 0 <= k < m and 0 <= l < n:
                    new_neighbors[i] += [(k, l)]
        return new_neighbors

    def get_next_moves(self):
        """
        Function to be overridden by the players
        Returns a list of the different moves
        """
        pass

    def __process_update(self):
        number_of_moves = self.__receive_data(1, "1B")[0]
        upd_commands_raw = self.__receive_data(
            number_of_moves * 5, "{}B".format(number_of_moves * 5)
        )
        upd_commands = list(self.__grouper(5, upd_commands_raw))
        self.grid.update_grid(upd_commands)

    def __send_moves(self, beasts, new_beasts):
        """ Creates and sends the MOV command """
        commands = []
        for i in range(len(beasts)):
            commands.append((beasts[i][0], beasts[i][1], beasts[i][2], new_beasts[i][0], new_beasts[i][1]))
        number_of_moves = len(commands)
        self.__sock.send("MOV".encode("ascii"))
        self.__sock.send(struct.pack("1B", number_of_moves))
        for move in commands:
            self.__sock.send(struct.pack("5B", *move))

    def run(self):
        """ Thread """
        self.__initialize_game()

        while True:
            header = self.__sock.recv(3).decode("ascii")
            if header == "END":
                self.__reset_game()
                self.__gameover = True
                # self.__initialize_game(nme=False)
            elif header == "BYE":
                print("[PLAYER - {}] - Goodbye !".format(
                    self.player_name.capitalize()
                ))
                self.__sock.close()
                return True
            elif header == "UPD":
                self.current_turn += 1
                print("[PLAYER - {}] - Turn {}".format(
                    self.player_name.capitalize(),
                    self.current_turn
                ))
                self.__process_update()
                (beasts, new_beasts) = self.get_next_moves()
                self.__send_moves(beasts, new_beasts) # Send data to the server
