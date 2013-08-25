var Game = function($, selector) {
    var game = {
        wrapper: $(selector),
    }

    game.board = game.wrapper.find('table tbody');
    game.scoreboard = game.wrapper.find('.scoreboard');

    game.template = function(data) {
        if (!game._template) {
            game._template = Handlebars.compile($('#table-template').html())
        }
        return game._template(data);
    }

    game.render = function() {
        game.board.html(game.template({}));
    }
    return game
}



$(function() {
    window.game = Game($, '.game');
    game.render();
});
