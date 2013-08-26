var Game = function(selector) {
    var game = {
        wrapper: $(selector),
    }

    game.board = game.wrapper.find('table tbody');
    game.scoreboard = game.wrapper.find('.scoreboard');
    game.squares = [0,0,0, 0,0,0, 0,0,0];
    game.human_mark = 1  /* 1 is human (X), 2 is computer (O), 0 is free */
    game.squareDisplayMapping = {0: '', 1: 'X', 2: 'O'}

    game.squaresDisplayValues = function() {
        return _.map(game.squares, function(i){ return game.squareDisplayMapping[i]; });
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

    game.endGame = function(winner) {
        if (!winner) {
            message = "Tie Game!";
        } else if (winner == 2) {
            message = "Computer Wins!";
        } else {
            message = "You Win!";
        }
        message += " <a href='#' onclick='game.restart();'>Try Again?</a>";
        
        $result = game.scoreboard.find('.result');
        game.scoreboard.find('.player').hide();
        $result.html(message).show();
    }

    game.restart = function() {
        game.squares = [0,0,0, 0,0,0, 0,0,0];
        game.scoreboard.find('.result').hide();
        game.scoreboard.find('.player').show();
        game.render();
        game.enable();
    }

    game.submit = function() {
        game.disable();
        var url = "/" + game.squares.join('') + "/";
        $.get(url).done(function(data) {
            // handle data
            game.squares = data.squares;
            if (data.is_over) {
                game.endGame(data.winner);
            } else {
                game.enable();
            }
            game.render();
        }).fail(function() {
            alert("I'm sorry. There was an error. I guess you win.");
        });
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
            $this = $(this);
            $this.hammer();
            $this.on('tap', function() {
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
