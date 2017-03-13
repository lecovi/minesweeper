"""
    minesweeper.models
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Description
    
    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
# Third-party imports
# LeCoVi imports


class Tile:
    """This class will represent each Tile."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_mine = False
        self.is_revealed = False
        self.is_marked = False
        self.mines_around = 0


class Board:
    """This class will represent the whole Board, a set of class:`Tile`"""

    def __init__(self, width=15, height=15, mines=30):
        self.width = width
        self.height = height
        self.mines = mines
        self.tiles = list()
        self._new_board()

    def _new_board(self):
        for x in range(self.height):
            self.tiles[x] = list()
            for y in range(self.width):
                new_tile = Tile(x=x, y=y)
                self.tiles[x].append(new_tile)

