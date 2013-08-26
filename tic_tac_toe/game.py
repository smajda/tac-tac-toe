from itertools import repeat
from random import choice
from textwrap import dedent


class GameException(Exception):
    pass


class Player(object):
    """
    A Tic-Tac-Toe player.

    Belongs to a game and sets a marker of
    Game.SQUARE_X or Game.SQUARE_O.

    Uses a "minimax" algorithm to choose best play.
    See maximized_move and minimized_move methods.
    """
    def __init__(self, marker, game):
        self.marker = marker
        self.game = game

    def __repr__(self):
        return "<Player {}>".format(self.marker)

    @property
    def opponent(self):
        return self.game.player_o if self.marker == self.game.SQUARE_X else self.game.player_x

    @property
    def squares(self):
        return self.game.indexes_for_marker(self.marker)

    def play(self, square=None):
        if square is None:
            square = self.pick_square()
        if square not in self.game.free_squares:
            raise GameException('Invalid square')
        self.game.set_square(marker=self.marker, square=square)

    def pick_square(self):
        # start off with some simple strategies for early moves
        # there's no advantage to expensive prediction and tic-tac-toe
        # has some well-established heuristics for early moves:
        # http://ostermiller.org/calc/tictactoe.html
        if self.game.current_move == 0:
            return choice(tuple(self.game.CORNERS))  # Start in a corner if first
        elif self.game.current_move == 1:
            # if they went corners, we go center, or vice versa
            if self.opponent.squares & self.game.CORNERS:
                return self.game.CENTER
            elif self.game.CENTER in self.opponent.squares:
                return choice(tuple(self.game.CORNERS))

        # Past first few moves, try to find maximized move
        square, _ = self.maximized_move()
        return square

    def maximized_move(self):
        """
        Find maximized move

        We're using a brute force "minimax" method of trying out
        possible versions of the game and picking the best move.
        I played around with several ways of doing this, but ended
        up basically borrowing/stealing Sarath Lakshman's implemention:

        http://www.sarathlakshman.com/2011/04/30/writing-a-tic-tac/

        It's the only one I tried (including my own) where I didn't
        get myself twisted in knots trying to make sense of it. :)

        Basically we loop through every free square on the board,
        play each square, then simulate our opponent doing the same,
        then our response, back and forth through every combination
        of the game, rewinding the state of the game as we go. We
        score each outcome along the way and pick the best one.

        I'm not thrilled with the 'go forward then rewind' approach,
        and I tried making up a fresh new game for each hypothetical
        path instead, but that ended up making my Game object too
        messy to accomodate keeping track of the players, plus it'd
        be even slower, so... this works.

        I understand you can also do cool things like rotating the board
        dramatically cut back on the number of possible games, which
        would make this much faster in the early rounds, but we'll
        leave that on the todo list for now.
        """
        best_score = None
        best_move = None

        for square in self.game.free_squares:
            self.game.set_square(marker=self.marker, square=square)

            if self.game.is_over():
                score = self.get_score()
            else:
                _, score = self.minimized_move()

            self.game.revert_last_move()

            if best_score is None or score > best_score:
                best_score = score
                best_move = square

        return best_move, best_score

    def minimized_move(self):
        "Find minimized move. See maximized_move for details."
        best_score = None
        best_move = None

        for square in self.game.free_squares:
            self.game.set_square(marker=self.opponent.marker, square=square)

            if self.game.is_over():
                score = self.get_score()
            else:
                _, score = self.maximized_move()

            self.game.revert_last_move()

            if best_score is None or score < best_score:
                best_score = score
                best_move = square

        return best_move, best_score

    def get_score(self):
        if self.game.winner:
            return 1 if self.game.winner == self else -1
        return 0


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
    two players and you can start to play. For each player, if
    no square is provided, it selects the optimal square.
    The game tracks the current player, so `game.play()`
    alternates its marker based on which player is playing.

    Because both players are computers, you can do this:

        game = Game()
        while not game.is_over():
            game.play()

    It will end in a tie every time. Alternatively,
    pass in an initial board and it will play the optimal
    game from that point on:

        Game(initial_board=[1,0,0, 0,0,0, 0,0,0])
        game.play()

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
        # set empty board or validate incoming board
        if initial_board is None:
            self.board = list(repeat(self.SQUARE_FREE, 9))
        elif self.is_valid_board(initial_board):
            self.board = initial_board
        else:
            raise GameException('Invalid initial board')
        self.player_x = Player(marker=self.SQUARE_X, game=self)
        self.player_o = Player(marker=self.SQUARE_O, game=self)
        self.history = []
        self.winner = None

    @classmethod
    def is_valid_board(cls, board):
        valid_items = {cls.SQUARE_FREE, cls.SQUARE_X, cls.SQUARE_O}
        try:
            all_valid = all(i in valid_items for i in board)
        except TypeError:
            return False  # would happen if board not iterable
        len_nine = len(board) == 9
        return all((all_valid, len_nine))

    def indexes_for_marker(self, marker):
        return {index for index, item in enumerate(self.board) if item == marker}

    x_squares = property(lambda self: self.indexes_for_marker(self.SQUARE_X))
    o_squares = property(lambda self: self.indexes_for_marker(self.SQUARE_O))
    free_squares = property(lambda self: self.indexes_for_marker(self.SQUARE_FREE))

    def check_status(self):
        "See if either player has won, if the game is a tie, or if it's still going"
        # TODO I suspect the way I'm checking for wins is slowing my game down,
        # especially in Player's maximized/minimized_move methods.
        # OTOH, sets are the clearest, most readable way to do this...
        for pattern in self.WINS:
            if pattern.issubset(self.x_squares):
                self.winner = self.player_x
                return self.STATUS_X  # X has winning set
            if pattern.issubset(self.o_squares):
                self.winner = self.player_o
                return self.STATUS_O  # O has winning set

        # No winner, so return playing or tied if no squares left
        return self.STATUS_PLAYING if self.free_squares else self.STATUS_TIED

    def is_over(self):
        "Updates status and return True if the game is over (in tie or victory)"
        status = self.check_status()
        return status != self.STATUS_PLAYING

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
        self.history.append(square)

    def revert_last_move(self):
        last_move = self.history.pop()
        self.board[last_move] = self.SQUARE_FREE
        self.winner = None

    def play(self, square=None):
        self.current_player.play(square)
        return self.check_status()


if __name__ == '__main__':

    #game = Game()
    #game.play(0); game.print_board()
    #game.play(4); game.print_board()
    #game.play(3); game.print_board()
    #game.play(1); game.print_board()
    #game.play(6); game.print_board()

    #game = Game(initial_board=[1,0,2, 1,2,0, 0,0,0])
    #game.print_board()

    #game = Game()
    game = Game(initial_board=[0,0,1, 0,2,1, 0,0,0])
    while not game.is_over():
        game.play(); game.print_board()  # Tie every time!

    #import IPython; IPython.embed()
