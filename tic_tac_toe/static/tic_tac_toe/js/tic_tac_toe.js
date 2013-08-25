var Game = function(selector) {
    var game = {
        wrapper: $(selector),
    }

    game.board = game.wrapper.find('table tbody');
    game.scoreboard = game.wrapper.find('.scoreboard');
    game.squares = [1,0,0, 1,2,0, 0,0,0];
    game.human_mark = 1  /* 1 is human (X), 2 is computer (O), 0 is free */

    game.squaresDisplayValues = function() {
        display_map = {0: ' ', 1: 'X', 2: 'O'}
        return _.map(game.squares, function(i){ return display_map[i]; });
    }

    game.play = function(index, marker) {
        game.squares[index] = marker;
        game.render();
        game.submit();
    }

    game.disable = function() {
        $('.scoreboard .computer').addClass('active')
        $('.scoreboard .human').removeClass('active')
    }

    game.enable = function () {
        $('.scoreboard .human').addClass('active')
        $('.scoreboard .computer').removeClass('active')
    }

    game.submit = function() {
        game.disable();
    }

    game.template = function(data) {
        if (!game._template) {
            game._template = Handlebars.compile($('#table-template').html())
        }
        return game._template(data);
    }

    game.render = function() {
        game.board.html(game.template({squares: game.squaresDisplayValues()}));
        game.bindClicks();
    }

    game.bindClicks = function() {
        game.board.find('td').each(function() {
            $(this).on('click', function() {
                $square = $(this);
                // do nothing if they click on already used squares
                used = $square.hasClass('O') || $square.hasClass('X');
                computers_turn = game.scoreboard.find('.computer').hasClass('active');
                if (used || computers_turn) {
                    return;
                }

                var id = $square.data('id')
                game.play(id, game.human_mark);
            });
        });
    }

    game.render();
    return game
}

$(function() {
    window.game = Game('.game');
});
