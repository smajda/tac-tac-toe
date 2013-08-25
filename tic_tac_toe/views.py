import json

from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.views.generic import TemplateView

from game import Game, GameException


index = TemplateView.as_view(template_name='tic_tac_toe/game.html')


def play(request, board):
    if request.method != 'GET':
        raise HttpResponseNotAllowed(['GET'])

    board = [int(i) for i in board]  # url validates board only has 0, 1, 2's.
    game = Game(initial_board=board)
    is_over = game.is_over()
    if not is_over:
        game.play()
        is_over = game.is_over()
    data = {
        'squares': game.board,
        'is_over': is_over,
        'winner': game.winner.marker if game.winner else None,
    }
    return HttpResponse(json.dumps(data), content_type="application/json")
