from itertools import repeat
from textwrap import dedent


class GameException(Exception):
    pass


class Player(object):
    """
    A Tic-Tac-Toe player.

    Belongs to a game and sets a marker of
    Game.SQUARE_X or Game.SQUARE_O
    """
    def __init__(self, marker, game):
        self.marker = marker
        self.game = game

    def __repr__(self):
        return "<Player {}>".format(self.marker)

    def play(self, square):
        # TODO if square is None, pick optimal move
        if square not in self.game.free_squares:
            raise GameException('Invalid square')
        self.game.set_square(marker=self.marker, square=square)


class Game(object):
    """
    This is a Tic-Tac-Toe game.

    Our board is a simple list if 9 ints of 0, 1, or 2, i.e.:

        board = [
            1, 0, 2,
            1, 2, 0,
            1, 0, 0,
        ]

    All you do is pass in an initial board and it instantiates
    two players and you can start to play. The game tracks
    the current player, so `game.play()` alternates its
    mark based on which player is playing.
    """
    # board markers
    SQUARE_FREE = 0
    SQUARE_X = 1
    SQUARE_O = 2

    # game status values
    STATUS_PLAYING = 0
    STATUS_TIED = 1
    STATUS_X = 2
    STATUS_O = 3

    # info about the board
    CENTER = 4
    CORNERS = {0, 2, 6, 8}
    WINS = (
        {0, 1, 2}, {0, 3, 6},
        {6, 7, 8}, {2, 5, 8},
        {3, 4, 5}, {1, 4, 7},
        {0, 4, 8}, {2, 4, 6},
    )

    def __init__(self, initial_board=None):
        self.board = initial_board or list(repeat(self.SQUARE_FREE, 9))
        self.player_x = Player(marker=self.SQUARE_X, game=self)
        self.player_o = Player(marker=self.SQUARE_O, game=self)
        self.winner = None

    def indexes_for_marker(self, marker):
        return {index for index, item in enumerate(self.board) if item == marker}

    x_squares = property(lambda self: self.indexes_for_marker(self.SQUARE_X))
    o_squares = property(lambda self: self.indexes_for_marker(self.SQUARE_O))
    free_squares = property(lambda self: self.indexes_for_marker(self.SQUARE_FREE))

    @property
    def status(self):
        "See if either player has won, if the game is a tie, or if it's still going"
        for pattern in self.WINS:
            if pattern.issubset(self.x_squares):
                self.winner = self.player_x
                return self.STATUS_X  # X has winning set
            if pattern.issubset(self.o_squares):
                self.winner = self.player_o
                return self.STATUS_O  # O has winning set

        # No winner, so return playing or tied if no squares left
        return self.STATUS_PLAYING if self.free_squares else self.STATUS_TIED

    @property
    def game_over(self):
        "Just a shortcut to see if the game is over yet (in a tie or victory)"
        return self.status != self.STATUS_PLAYING

    @property
    def current_move(self):
        "Return number of current move, 0 through 9"
        return 9 - len(self.free_squares)

    @property
    def current_player(self):
        "Return current player"
        return self.player_x if self.current_move % 2 == 0 else self.player_o

    def print_board(self):
        "Helpful while developing to be able to print this out"
        print(dedent("""
            {} {} {}
            {} {} {}
            {} {} {}
        """.format(*self.board)))

    def set_square(self, marker, square):
        self.board[square] = marker

    def play(self, square):
        self.current_player.play(square)
        if self.game_over:
            print "{} wins!".format(self.winner) if self.winner else "Darn cat!"

if __name__ == '__main__':

    #game = Game()
    #game.play(0); game.print_board()
    #game.play(4); game.print_board()
    #game.play(3); game.print_board()
    #game.play(1); game.print_board()
    #game.play(6); game.print_board()

    game = Game(initial_board=[1,0,2, 1,2,0, 0,0,0])
    game.print_board()
    game.play(6)

    #import IPython; IPython.embed()
