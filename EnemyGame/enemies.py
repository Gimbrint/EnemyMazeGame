import game_object
from draw_board import SquareFlags
from random import randint
from assets import AssetTypes

class Enemy1(game_object.GameObject):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, SquareFlags.ENEMY)
        self.set_image(AssetTypes.ENEMY_1)

    def move(self):
        rng = randint(0, 3)

        while not self.game.inside_board(self.x + self.game.config.Directions_plus[rng][0], self.y + self.game.config.Directions_plus[rng][1]):
            rng = randint(0, 3)

        super().move(self.game.config.Directions_plus[rng][0], self.game.config.Directions_plus[rng][1])

class Enemy2(game_object.GameObject):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, SquareFlags.ENEMY)
        self.set_image(AssetTypes.ENEMY_2)

        self.last_cost = [None] * self.game.w
        for x in range(0, self.game.w):
            self.last_cost[x] = [0] * 8

    def move(self):
        processed = self.game.dijkstra.dijkstra(self.game.player.x, self.game.player.y)
        #self.game.dijkstra.print_path(processed, self.game.player.x, self.game.player.y, self.x, self.y)

        path = processed[self.y][self.x]

        print(path[0] - self.x, self.y - path[1])
        super().move(path[0] - self.x, path[1] - self.y)

class Enemy3(game_object.GameObject):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, SquareFlags.ENEMY)
        self.set_image(AssetTypes.ENEMY_3)

    def move(self):
        pass