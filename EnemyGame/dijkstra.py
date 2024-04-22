import math
import heapq
from draw_board import SquareFlags

class Dijkstra():
    def __init__(self, game):
        self.game = game

    def dijkstra(self, startx, starty):
        w = self.game.w
        h = self.game.h
        field = self.game.field
        visited = [[False for i in range(w)] for j in range(h)]
        dist = [[math.inf for i in range(w)] for j in range(h)]
        prev = [[(0,0) for i in range(w)] for j in range(h)]
        dist[starty][startx] = 0
        direct = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        q = [] # priority queue
        heapq.heappush(q, (0, startx, starty))
        while q:
            #changed = False
            curr = heapq.heappop(q)
            currx = curr[1]
            curry = curr[2]
            if visited[curry][currx]:
                continue
            if field[currx][currx] & SquareFlags.WALL: # akmeņi
                continue
            visited[curry][currx] = True
            for dx, dy in direct:
                x = dx + currx
                y = dy + curry
                if 0 <= x < w and 0 <= y < h and not visited[y][x]:
                    if dist[y][x] > dist[curry][currx]+field[x][y]:
                        dist[y][x] = dist[curry][currx]+field[x][y]
                        prev[y][x] = (currx, curry)
                        #changed = True
                    heapq.heappush(q, (dist[y][x], x, y) )
            #print( len(q) )
            #if changed:
            #    print_grid( dist )
            #    print()
        #print_grid( visited )
        #print_grid( dist )
        return prev

    def print_path(self, path, startx, starty, endx, endy):
        w = self.game.w
        h = self.game.h
        grid = [["_" for i in range(w)] for j in range(h)]
        x = endx
        y = endy
        grid[y][x] = "E"
        while x != startx or y != starty:
            x, y = path[y][x]

            grid[y][x] = "X"

        grid[y][x] = "S"
        self.print_grid( grid )

    def print_grid(self, grid):
        w = self.game.w
        h = self.game.h
        for i in range(h):
            for j in range(w):
                print(grid[i][j],end="\t")
            print()
