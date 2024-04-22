import tkinter as tk
from draw_board import SquareFlags

class GameObject():
    def __init__(self, game, x, y, square_flag):
        self.game = game

        self.x = x
        self.y = y

        self.square_flag = square_flag
        self.game.field[x][y] |= self.square_flag
        
        self.image = None
        self.imageid = -1
        
        self.energy = 100

    def move(self, dx, dy):
        self.game.field[self.x][self.y] ^= self.square_flag

        if (self.x + dx > 0 and self.x + dx < self.game.w):
            self.x = self.x + dx
        if (self.y + dy > 0 and self.y + dy < self.game.h):
            self.y = self.y + dy

        self.game.field[self.x][self.y] |= self.square_flag

        self.game.window.canvas.move(self.imageid, dx*self.game.config.cell_size, dy*self.game.config.cell_size)

        self.check_square_cost(self.x, self.y)

    def change_energy(self, de):
        self.energy += de

    def check_square_cost(self, x, y):
        # If the square has food, eat it!!!
        if self.game.field[self.x][self.y] & SquareFlags.FOOD:
            self.energy += self.game.config.energy_food
            self.game.field[self.x][self.y] ^= SquareFlags.FOOD
            self.game.window.canvas.delete(self.game.food_grid[self.x][self.y])
            self.game.food_grid[self.x][self.y] = -1
        # Else check what kind of floor this and remove the energy it takes to cross
        elif self.game.field[x][y] & 3 == SquareFlags.FLOOR_1:
            #print("Deducted cost of floor 1")
            self.energy -= self.game.config.cost_floor_1
        elif self.game.field[x][y] & 3 == SquareFlags.FLOOR_2:
            #print("Deducted cost of floor 2")
            self.energy -= self.game.config.cost_floor_2
        elif self.game.field[x][y] & 3 == SquareFlags.FLOOR_3:
            #print("Deducted cost of floor 3")
            self.energy -= self.game.config.cost_floor_3

    def set_image(self, type):
        self.image = self.game.window.assets.images[int(type)]
        self.imageid = self.game.window.canvas.create_image(
            self.x*self.game.config.cell_size,
            self.y*self.game.config.cell_size,
            anchor=tk.NW, image=self.image
        )
        return self.imageid
    
    def die(self):
        self.game.window.canvas.delete(self.imageid)