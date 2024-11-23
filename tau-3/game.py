import random
import os

class Game:
    """
    Poruszasz się graczem za pomocą klawiszy w, s, a, d. Aby wyjść, naciśnij q.
    Gra kończy się, gdy gracz znajdzie skarb.
    """
    BOARD_SIZE = 5
    PLAYER = 'P'
    OBSTACLE = 'x'
    TREASURE = 'T'
    EMPTY = ' '

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.player_position = self.place_player_position()
        self.treasure_position = self.place_treasure_position()
        self.board = self.create_board()

    def place_player_position(self):
        """Losuje pozycję gracza"""
        x = random.randint(0, self.BOARD_SIZE - 1)
        return [x, 0]

    def place_treasure_position(self):
        """Losuje pozycję skarbu"""
        x = random.randint(0, self.BOARD_SIZE - 1)
        return [x, self.BOARD_SIZE - 1]

    def create_board(self):
        """Tworzy planszę z przeszkodami"""
        board = [[self.EMPTY for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.place_obstacles(board)
        return board

    def place_obstacles(self, board):
        """Losuje pola, na których będą przeszkody"""
        for i in range(1, 4):
            x1, y = random.randint(0, self.BOARD_SIZE-1), i
            board[x1][y] = self.OBSTACLE
            x2, y = random.randint(0, self.BOARD_SIZE - 1), i
            while board[x2][y] != self.EMPTY:
                x2, y = random.randint(0, self.BOARD_SIZE - 1), i
            board[x2][y] = self.OBSTACLE

    def print_board(self):
        """Wyświetla planszę z pozycją gracza i skarbu w terminalu"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print('_' * (self.BOARD_SIZE + 2))
        for i in range(self.BOARD_SIZE):
            print('|', end='')
            for j in range(self.BOARD_SIZE):
                if self.player_position == [i, j]:
                    print(self.PLAYER, end='')
                elif self.treasure_position == [i, j]:
                    print(self.TREASURE, end='')
                else:
                    print(self.board[i][j], end='')
            print('|')
        print('_' * (self.BOARD_SIZE + 2))

    def move_player(self, move):
        """Logika obsługująca ruch gracza"""
        x, y = self.player_position
        if move == 'w' and x > 0 and self.board[x-1][y] != self.OBSTACLE:
            self.player_position = [x-1, y]
        elif move == 's' and x < self.BOARD_SIZE-1 and self.board[x+1][y] != self.OBSTACLE:
            self.player_position = [x+1, y]
        elif move == 'a' and y > 0 and self.board[x][y-1] != self.OBSTACLE:
            self.player_position = [x, y-1]
        elif move == 'd' and y < self.BOARD_SIZE-1 and self.board[x][y+1] != self.OBSTACLE:
            self.player_position = [x, y+1]

    def check_win(self):
        """Logika sprawdzająca, czy gracz zdobył skarb"""
        return self.player_position == self.treasure_position