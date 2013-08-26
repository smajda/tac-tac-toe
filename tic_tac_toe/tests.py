import unittest

from .game import Game, GameException

class TicTacToeTest(unittest.TestCase):
    "Basic tests for Tic Tac Toe game"
    def testEmptyGame(self):
        "Empty game, computer vs computer, always ties"
        game = Game()
        while not game.is_over():
            game.play()
        # game should be over and tied
        self.assertEqual(game.is_over(), True)
        self.assertEqual(game.winner, None)
        self.assertEqual(game.check_status(), game.STATUS_TIED)

    def testBadBoard(self):
        "Bad board raises error"
        self.assertRaises(GameException, Game, initial_board=[1, 2, 3, 4])

    def testPlayerTurns(self):
        "Check player turns alternate properly"
        game = Game(initial_board=[0,0,1, 0,0,0, 0,0,0])
        self.assertEqual(game.current_player.marker, 2)
        game.play()
        self.assertEqual(game.current_player.marker, 1)
        game.play()
        self.assertEqual(game.current_player.marker, 2)

    def testWin(self):
        "Pass in a board one play away from winning, should take it"
        game = Game(initial_board=[1,2,0, 1,2,0, 0,0,0])
        self.assertEqual(game.current_player.marker, 1)
        game.play()
        self.assertEqual(game.check_status(), game.STATUS_X)
        self.assertEqual(game.winner, game.player_x)

    def testManualPlay(self):
        "Test manually playing some squares, with invalid value"
        game = Game()
        game.play(0)
        game.play(4)
        game.play(1)
        self.assertTrue(game.x_squares, {0, 1})  # x's squares
        self.assertTrue(game.o_squares, {4})  # o's squares
        self.assertRaises(GameException, game.play, 42)  # invalid square
