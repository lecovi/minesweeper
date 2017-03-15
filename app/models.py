"""
    minesweeper.models
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Description
    
    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
from random import choice
# Third-party imports
from flask_sqlalchemy import SQLAlchemy
# LeCoVi imports


db = SQLAlchemy()


class GameOverException(Exception):
    pass


class Tile(db.Model):
    """This class will represent each Tile."""
    __tablename__ = 'tiles'

    id = db.Column(db.Integer, primary_key=True, index=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    has_mine = db.Column(db.Boolean, default=False, nullable=False)
    is_revealed = db.Column(db.Boolean, default=False, nullable=False)
    is_marked = db.Column(db.Boolean, default=False, nullable=False)
    mines_around = db.Column(db.Integer, default=0, nullable=False)
    board_id = db.Column(db.ForeignKey('boards.id'))


class Board(db.Model):
    """This class will represent the whole Board, a set of class:`Tile`"""

    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True, index=True)
    width = db.Column(db.Integer, nullable=False, default=20)
    height = db.Column(db.Integer, nullable=False, default=15)
    mines = db.Column(db.Integer, nullable=False, default=30)

    tiles = list()

    @classmethod
    def get_by(cls, board_id):
        board = db.session.query(Board).filter_by(id=board_id).first()
        board.tiles = list()
        for x in range(board.width):
            board.tiles.append(list())
            for y in range(board.height):
                tile = board.get_tile(x=x, y=y)
                board.tiles[x].append(tile)
        return board

    def create_tiles(self):
        for y in range(self.height):
            row = list()
            for x in range(self.width):
                new_tile = Tile(x=x, y=y, board_id=self.id)
                db.session.add(new_tile)
                db.session.commit()
                row.append(new_tile)
            self.tiles.append(row)

    def get_tile(self, x, y):
        return db.session.query(Tile).filter_by(board_id=self.id, x=x,
                                                y=y).first()

    def set_mines(self):
        mines_left = self.mines
        while mines_left > 0:
            random_row = choice(range(self.width))
            random_col = choice(range(self.height))
            tile = self.get_tile(x=random_row, y=random_col)
            if not tile.has_mine:
                tile.has_mine = True
            mines_left -= 1

    def set_mines_around(self):
        for row in self.tiles:
            for tile in row:
                for neighbour in self.get_neighbours(tile=tile):
                    if neighbour.has_mine:
                        tile.mines_around += 1

    def get_neighbours(self, tile):
        neighbours_list = list()
        if tile.y == 0:
            neighbours_list.append(self.get_tile(tile.x, tile.y + 1))
            if tile.x == 0:
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y + 1))
            elif tile.x == self.width - 1:
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y))
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y + 1))
            else:
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y))
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y + 1))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y + 1))
        elif tile.y == self.height - 1:
            neighbours_list.append(self.get_tile(tile.x, tile.y - 1))
            if tile.x == 0:
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y - 1))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y))
            elif tile.x == self.width - 1:
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y - 1))
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y))
            else:
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y - 1))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y - 1))
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y))
        else:
            neighbours_list.append(self.get_tile(tile.x, tile.y - 1))
            neighbours_list.append(self.get_tile(tile.x, tile.y + 1))
            if tile.x == 0:
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y - 1))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y + 1))
            elif tile.x == self.width - 1:
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y - 1))
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y))
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y + 1))
            else:
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y - 1))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y - 1))
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y))
                neighbours_list.append(self.get_tile(tile.x - 1, tile.y + 1))
                neighbours_list.append(self.get_tile(tile.x + 1, tile.y + 1))
        return neighbours_list

    def reveal_zone(self, tile):
        neighbours = self.get_neighbours(tile=tile)
        for neighbour in neighbours:
            if not neighbour.is_revealed:
                self.reveal_tile(x=neighbour.x, y=neighbour.y)

    def reveal_tile(self, x, y):
        tile = self.get_tile(x, y)
        if not tile.is_marked and not tile.is_revealed:
            if tile.has_mine:
                raise GameOverException('boom!')
            tile.is_revealed = True
            if tile.mines_around == 0:
                self.reveal_zone(tile)

    def mark(self, x, y):
        tile = self.get_tile(x, y)
        if not tile.is_revealed:
            tile.is_marked = not tile.is_marked
