"""
    minesweeper.routes
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Description
    
    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
# Third-party imports
from flask import Blueprint, render_template
# LeCoVi imports
from .models import db, Board, GameOverException

mines = Blueprint('mines', __name__)


@mines.route('/')
def index():
    return render_template('index.html')


@mines.route('/new')
def new_game():
    board = Board()
    db.session.add(board)
    db.session.commit()
    board.create_tiles()
    db.session.commit()
    board.set_mines()
    db.session.commit()
    board.set_mines_around()
    db.session.commit()
    return render_template('new_game.html', board=board)


@mines.route('/reveal/<int:board_id>/<int:x>/<int:y>')
def reveal(board_id, x, y):
    board = Board.get_by(board_id)
    try:
        board.reveal_tile(x, y)
    except GameOverException:
        return render_template('game_over.html', board=board, x=x, y=y)
    db.session.commit()
    return render_template('new_game.html', board=board)
