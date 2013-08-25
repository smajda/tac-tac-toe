from django.views.generic import TemplateView


index = TemplateView.as_view(template_name='tic_tac_toe/game.html')

def tic_tac_toe_play(request, board):
    pass  # TODO
