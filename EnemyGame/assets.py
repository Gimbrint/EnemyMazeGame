from PIL import Image, ImageTk
from enum import IntEnum
 
class AssetTypes(IntEnum):
    PLAYER = 0
    ENEMY_1 = 1
    ENEMY_2 = 2
    ENEMY_3 = 3
    FOOD = 4
    DRINK = 5
    EDGE = 6
    WALL = 7
    FLOOR_1 = 8
    FLOOR_2 = 9
    FLOOR_3 = 10

class Assets:
    def __init__(self, game, tk):
        self.game = game
        self.tk = tk

        self.images = [None] * 11
        self.images[AssetTypes.PLAYER] = ImageTk.PhotoImage(Image.open("assets/player.png").resize((game.config.cell_size, game.config.cell_size)))
        self.images[AssetTypes.ENEMY_1] = ImageTk.PhotoImage(Image.open("assets/enemy_1.png"))
        self.images[AssetTypes.ENEMY_2] = ImageTk.PhotoImage(Image.open("assets/enemy_2.png"))
        self.images[AssetTypes.ENEMY_3] = ImageTk.PhotoImage(Image.open("assets/enemy_3.png"))
        self.images[AssetTypes.FOOD] = ImageTk.PhotoImage(Image.open("assets/food.png"))
        # self.images[AssetTypes.DRINK] = ImageTk.PhotoImage(Image.open("assets/drink.png"))
        self.images[AssetTypes.EDGE] = ImageTk.PhotoImage(Image.open("assets/edge.png").resize((game.config.cell_size, game.config.cell_size)))
        self.images[AssetTypes.WALL] = ImageTk.PhotoImage(Image.open("assets/wall.png").resize((game.config.cell_size, game.config.cell_size)))
        self.images[int(AssetTypes.FLOOR_1)] = ImageTk.PhotoImage(Image.open("assets/floor_1.png").resize((game.config.cell_size+4, game.config.cell_size+4)))
        self.images[int(AssetTypes.FLOOR_2)] = ImageTk.PhotoImage(Image.open("assets/floor_2.png").resize((game.config.cell_size+4, game.config.cell_size+4)))
        self.images[int(AssetTypes.FLOOR_3)] = ImageTk.PhotoImage(Image.open("assets/floor_3.png").resize((game.config.cell_size+4, game.config.cell_size+4)))