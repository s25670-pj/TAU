from game import Game

def test_initial_position():
    """Sprawdza, czy początkowa pozycja gracza nie jest taka sama jak pozycja skarbu"""
    game = Game()
    assert game.player_position != game.treasure_position

def test_game_identical_when_seed_the_same():
    """
    Sprawdza, czy gra losuje te same pozycje gracza, skarbu i przeszkód,
    gdy użyte jest to samo ziarno losowe
    """
    game1 = Game(seed=1)
    game2 = Game(seed=1)

    assert (game1.player_position == game2.player_position and
            game1.treasure_position == game2.treasure_position and
            game1.board == game2.board), "Game is not identical when seed is the same"

def test_player_position_is_different_when_seed_is_different():
    """Sprawdza, czy pozycja gracza różni się, gdy użyte są różne ziarna losowe"""
    game1 = Game(seed=1)
    game2 = Game(seed=2)

    assert game1.player_position != game2.player_position, \
        "Player position is not different when seed is different"

def test_treasure_position_is_different_when_seed_is_different():
    """Sprawdza, czy pozycja skarbu różni się, gdy użyte są różne ziarna losowe"""
    game1 = Game(seed=1)
    game2 = Game(seed=2)

    assert game1.treasure_position != game2.treasure_position, \
        "Treasure position is not different when seed is different"

def test_obstacles_position_is_different_when_seed_is_different():
    """Sprawdza, czy pozycje przeszkód różnią się, gdy użyte są różne ziarna losowe"""
    game1 = Game(seed=1)
    game2 = Game(seed=2)

    assert game1.board != game2.board, \
        "Obstacles positions is not different when seed is different"

def test_move_up():
    """Sprawdza, czy gracz poprawnie porusza się w górę"""
    game = Game(seed=1)
    initial_position = game.player_position.copy()
    x, y = initial_position
    game.move_player('w')
    assert game.player_position != initial_position and game.player_position == [x-1, y], \
        "Player should have moved up"

def test_move_down():
    """Sprawdza, czy gracz poprawnie porusza się w dół"""
    game = Game(seed=1)
    initial_position = game.player_position.copy()
    x, y = initial_position
    game.move_player('s')
    assert game.player_position != initial_position and game.player_position == [x+1, y], \
        "Player should have moved down"

def test_move_right():
    """Sprawdza, czy gracz poprawnie porusza się w prawo"""
    game = Game(seed=1)
    initial_position = game.player_position.copy()
    x, y = initial_position
    game.move_player('d')
    assert game.player_position != initial_position and game.player_position == [x, y+1], \
        "Player should have moved to right"

def test_move_left():
    """Sprawdza, czy gracz poprawnie porusza się w lewo"""
    game = Game(seed=1)
    game.move_player('d')
    initial_position = game.player_position.copy()
    x, y = initial_position
    game.move_player('a')
    assert game.player_position != initial_position and game.player_position == [x, y-1], \
        "Player should have moved to the left"


def test_left_border():
    """Sprawdza, czy gracz nie przekroczy lewej krawędzi planszy"""
    game = Game(seed=1)
    initial_position = game.player_position.copy()
    game.move_player('a')
    assert game.player_position == initial_position, "Player should not cross the left border"

def test_upper_border():
    """Sprawdza, czy gracz nie przekroczy górnej krawędzi planszy"""
    game = Game(seed=1)
    game.move_player('w')
    initial_position = game.player_position.copy()
    game.move_player('w')
    assert game.player_position == initial_position, "Player should not cross the upper border"

def test_lower_border():
    """Sprawdza, czy gracz nie przekroczy dolnej krawędzi planszy"""
    game = Game(seed=1)
    for _ in range(3):
        game.move_player('s')
    initial_position = game.player_position.copy()
    game.move_player('s')
    assert game.player_position == initial_position, "Player should not cross the lower border"

def test_right_border():
    """Sprawdza, czy gracz nie przekroczy prawej krawędzi planszy"""
    game = Game(seed=1)
    for _ in range(2):
        game.move_player('d')
    game.move_player('s')
    for _ in range(2):
        game.move_player('d')
    initial_position = game.player_position.copy()
    game.move_player('d')
    assert game.player_position == initial_position, "Player should not cross the right border"

def test_obstacle():
    """Sprawdza, czy gracz nie przekroczy przeszkody"""
    game = Game(seed=1)
    for _ in range(2):
        game.move_player('d')
    initial_position = game.player_position.copy()
    game.move_player('d')
    assert game.player_position == initial_position, \
        "Player should not cross obstacle"

def test_get_treasure():
    """Sprawdza, czy gra kończy się, gdy gracz zdobędzie skarb"""
    game = Game(seed=1)
    assert not game.check_win(), "Player should not win in the beginning of the game"
    for _ in range(3):
        game.move_player('s')
    for _ in range(4):
        game.move_player('d')
    assert game.check_win(), "Player should win when he gets on treasure position"
