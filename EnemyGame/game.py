import tkinter as tk
import draw_board
import player
import enemies
import dijkstra
from assets import AssetTypes
from draw_board import SquareFlags, is_floor, has_entity
from random import random, randint
from enum import IntEnum

class Config:
    def __init__(self):
        self.num_enemies = 3
        self.cell_size = 32

        # The amount of energy the floor removes
        self.cost_floor_1 = 3
        self.cost_floor_2 = 9
        self.cost_floor_3 = 27

        # Food settings
        self.max_food = 20
        self.energy_food = 45

        # Directions in a plus shape
        #     #
        #   # O #
        #     #
        self.Directions_plus = [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]

class Game:
    # Initialize game settings
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.field = []

        # Current game state
        self.game_state = GameStates.START
        self.turn_i = 1

        self.food_grid = [[-1 for j in range(self.h)] for i in range(0, self.w)]
        self.num_active_food = 0

        self.config = Config()
        self.window = draw_board.Window(self)
        self.dijkstra = dijkstra.Dijkstra(self)

    def run_game(self):
        self.create_field()
        
        self.window.draw_field()

        # Create player
        pos = self.choose_xy()
        self.player = player.Player(self, pos[0], pos[1])

        self.enemies = []
        for i in range(0, self.config.num_enemies):
            pos = self.choose_xy()
            
            rng = random()

            if rng < 1/3:
                self.enemies.append(enemies.Enemy1(self, pos[0], pos[1]))
            elif rng < 2/3:
                self.enemies.append(enemies.Enemy2(self, pos[0], pos[1]))
            else:
                self.enemies.append(enemies.Enemy3(self, pos[0], pos[1]))

        # Begin detection of keyboard inputs'
        self.window.tk.bind("<Key>", self.process_turn)

        self.window.tk.mainloop()

    def create_field(self):
        self.field = [[SquareFlags.EDGE for i in range(self.h)] for j in range(self.w)]

        for x in range(1, self.h - 1):
            for y in range(1, self.h - 1):
                rng = random()

                if rng < 1/4:
                    self.field[x][y] = SquareFlags.FLOOR_1
                elif rng < 2/4:
                    self.field[x][y] = SquareFlags.FLOOR_2
                elif rng < 3/4:
                    self.field[x][y] = SquareFlags.FLOOR_3
                else:
                    self.field[x][y] = SquareFlags.WALL

        self.clean_field()
    
    def clean_field(self):
        for x in range(1, self.h - 1):
            for y in range(1, self.h - 1):
                is_disconnected = True

                for d in self.config.Directions_plus:
                    if self.inside_board(x + d[0], y + d[1]):
                        is_disconnected = False
                
                if is_disconnected:
                    self.field[x][y] = SquareFlags.WALL

    def choose_xy(self, condition=is_floor):
        x = randint(0, self.w-1)
        y = randint(0, self.h-1)

        while not condition(self.field[x][y]):
            x = randint(0, self.w-1)
            y = randint(0, self.h-1)

        return (x, y)
    
    def process_turn(self, e):
        if not self.player.move(e.keysym):
            return

        for enemy in self.enemies:
            enemy.move()

        # If this condition is satisfied, spawn food at random location
        if self.num_active_food <= self.config.max_food and self.turn_i % 2:
            self.spawn_food()

        self.turn_i += 1

    def spawn_food(self):
        pos = self.choose_xy(lambda s : is_floor(s) and not has_entity(s))

        self.field[pos[0]][pos[1]] |= SquareFlags.FOOD
        self.food_grid[pos[0]][pos[1]] = self.window.canvas.create_image(
            pos[0]*self.config.cell_size,
            pos[1]*self.config.cell_size,
            anchor=tk.NW,
            image=self.window.assets.images[int(AssetTypes.FOOD)]
        )

        self.num_active_food += 1

    def inside_board(self, x, y):
        return x > 0 and y > 0 and x < self.w - 1 and y < self.h - 1 and self.field[x][y] & SquareFlags.WALL == 0
    
class GameStates(IntEnum):
    START = 0,
    PLAY = 1,
    DEAD = 2,