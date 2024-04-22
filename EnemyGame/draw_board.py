from enum import IntEnum
import tkinter as tk
import main
import assets
from random import random

class Window:
    # Initialize the tkinter window instance
    def __init__(self, game):
        self.tk = tk.Tk()

        # Easy access
        self.game = game

        # Create new image asset class
        self.assets = assets.Assets(game, self.tk)

        # self.interface = label = Label(root, textvariable=var, relief=RAISED)
        # self.interface.pack()

        self.canvas = tk.Canvas(self.tk, width=game.config.cell_size*game.w, height=game.config.cell_size*game.h, background='gray75')
        self.canvas.pack()

    # Destory window instance when leaving
    def __del__(self):
        try:
            self.tk.destroy()
        except:
            pass

    def draw_field(self):
        # SquareFlag | AssetType | Offset
        check = [
            (SquareFlags.FLOOR_3, assets.AssetTypes.FLOOR_3, -2),
            (SquareFlags.FLOOR_2, assets.AssetTypes.FLOOR_2, -2),
            (SquareFlags.FLOOR_1, assets.AssetTypes.FLOOR_1, -2),
            (SquareFlags.WALL, assets.AssetTypes.WALL, 0),
        ]

        for c in check:
            for x in range(self.game.h):
                for y in range(self.game.h):
                    if self.has_flag(self.game.field[x][y], c[0]):
                        self.draw_square(x, y, c[1], c[2])

        for x in range(self.game.h):
            for y in range(self.game.h):
                if self.game.field[x][y] == 0:
                    self.draw_square(x, y, assets.AssetTypes.EDGE)

    def draw_square(self, x, y, type, offset=0):
        self.canvas.create_image(self.game.config.cell_size*(x + offset/32), self.game.config.cell_size*(y + offset/32), anchor=tk.NW,
            image=self.assets.images[int(type)])
        
    def has_flag(self, square, square_flag):
        return square & square_flag == square_flag

class SquareFlags(IntEnum):
    EDGE = 0
    FLOOR_1 = 1
    FLOOR_2 = 2
    FLOOR_3 = 3
    WALL = 4
    PLAYER = 8
    ENEMY = 16
    FOOD = 32
    DRINK = 64

def is_floor(square):
    return square & 3 != 0

def has_entity(square):
    return square & SquareFlags.PLAYER or square & SquareFlags.ENEMY or square & SquareFlags.FOOD