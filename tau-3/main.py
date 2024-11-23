import sys
import os
from game import Game

def get_keypress_linux():
    import termios  # pylint: disable=import-error,import-outside-toplevel
    import tty  # pylint: disable=import-error,import-outside-toplevel
    import contextlib  # pylint: disable=import-error,import-outside-toplevel

    @contextlib.contextmanager
    def raw_mode(file):
        old_attrs = termios.tcgetattr(file.fileno())
        new_attrs = old_attrs[:]
        new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
        try:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
            yield
        finally:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

    with raw_mode(sys.stdin):
        tty.setcbreak(sys.stdin)
        return sys.stdin.read(1).lower()


def get_keypress_windows():
    import msvcrt  # pylint: disable=import-error,import-outside-toplevel
    return msvcrt.getch().decode().lower()


def main():
    game = Game()
    while True:
        game.print_board()
        if game.check_win():
            print('Wygrałeś!')
            break
        move = get_keypress_windows() if os.name == 'nt' else get_keypress_linux()
        if move in ['w', 's', 'a', 'd']:
            game.move_player(move)
        elif move == 'q':
            break


if __name__ == "__main__":
    main()