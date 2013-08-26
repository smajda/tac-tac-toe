import json
import unittest

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import Client

from .game import Game, GameException


class TicTacToeGameTest(unittest.TestCase):
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


def url_for_board(board):
    return reverse('tic_tac_toe_play', args=(board, ))


class TicTacToeAppTest(unittest.TestCase):
    "Tests for the tac_tac_toe django app"
    def setUp(self):
        self.client = Client()

    def testIndexView(self):
        """
        For now, just do a simple 200.
        We'd need selenium or something to interact with this page.
        """
        url = reverse('tic_tac_toe_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def testFirstPlay(self):
        "Try a first move, make sure the response is correct"
        response = self.client.get(url_for_board('100000000'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['is_over'], False)
        self.assertEqual(data['winner'], None)
        # for this initial board, the response should always be
        # to take the center square:
        self.assertEqual(data['squares'], [1,0,0, 0,2,0, 0,0,0])

    def testWinningPlay(self):
        "Give the game a board it can win. Make sure it does"
        response = self.client.get(url_for_board('201210000'))
        data = json.loads(response.content)
        self.assertEqual(data['is_over'], True)
        self.assertEqual(data['winner'], 1)
        self.assertEqual(data['squares'], [2,0,1, 2,1,0, 1,0,0])

    def testBadRequests(self):
        self.assertRaises(NoReverseMatch, url_for_board, '00100200')
        self.assertRaises(NoReverseMatch, url_for_board, 'aoeu')
