import pygame
from mazeSolver import *

class MazeSolverDeadend(MazeSolver):
    def __init__(self, maze):
        super().__init__(maze)

        self.filled = [[False for y in range(self.height)] for x in range(self.width)]
        self.complete = False

    def _neighbours(self, x, y):
        '''
        count number of neighbours that are walls/deadends
        '''
        count = 0
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            fx = x + dx
            fy = y + dy
            if fx < 0 or fx >= self.width:
                continue
            elif fy < 0 or fy >= self.height:
                continue
            elif self.maze[fx][fy]:
                count += 1
            elif self.filled[fx][fy]:
                count += 1
        return count

    def step(self):
        '''
        take one loop through the maze and fill any dead ends
        '''
        if self.complete:
            return
        self.complete = True
        temp_filled = []
        for x in range(self.width):
            for y in range(self.height):
                if self.maze[x][y]:
                    continue
                if self._neighbours(x, y) >= 3:
                    temp_filled.append((x, y))
                    self.complete = False
        for x, y in temp_filled:
            self.filled[x][y] = True

        
    def draw(self, surface, scale, offset):
        '''
        draw the solving process on the maze
        '''
        for x in range(self.width):
            for y in range(self.height):
                if self.filled[x][y]:
                    display_x = x * scale[0] + offset[0]
                    display_y = y * scale[1] + offset[1]
                    pygame.draw.circle(surface, (0, 0, 0), (display_x, display_y), 3)