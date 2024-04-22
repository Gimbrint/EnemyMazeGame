import game_object
from assets import AssetTypes
from draw_board import SquareFlags

class Player(game_object.GameObject):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, SquareFlags.PLAYER)
        self.set_image(AssetTypes.PLAYER)

    def move(self, keysym):
        player_dir = None

        # Player up movement (W)
        if keysym == "Up":
            player_dir = (0, -1)
        # Player down movement (S)
        elif keysym == "Down":
            player_dir = (0, 1)
        # Player left movement (A)
        elif keysym == "Left":
            player_dir = (-1, 0)
        # Player right movement (D)
        elif keysym == "Right":
            player_dir = (1, 0)
        
        if player_dir == None or not self.game.inside_board(self.x + player_dir[0], self.y + player_dir[1]):
            return False

        super().move(player_dir[0], player_dir[1])
        return True