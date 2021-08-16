import pygame
from mazeSolver import *

class MazeSolverRecursive(MazeSolver):
    def __init__(self, maze):
        super().__init__(maze)

        self.current = self.start
        print(self.current, self.end)
        # set the state
        self.state = [[0 for y in range(self.height)] for x in range(self.width)]

    def _can_step(self, location):
        return not self.maze[location[0]][location[1]]
    
    def _in_path(self, location):
        return location in self.path

    def _valid_next_step(self, location):
        '''
        determine if the next attempted location is open and
        is not in the path previously traversed
        '''
        if not self._valid_loc(location):
            return False
        if not self._can_step(location):
            return False
        if self._in_path(location):
            return False
        return True

    def step(self):
        if self.complete or self.current == self.end:
            self.complete = True
            return

        cell_state = self.state[self.current[0]][self.current[1]]
        # move into the next state
        self.state[self.current[0]][self.current[1]] += 1

        if (cell_state >= 4):
            self.current = self.path.pop()
            return
        elif (cell_state == 0): # try left
            next_step = (self.current[0] + 1, self.current[1])
        elif (cell_state == 1): # try right
            next_step = (self.current[0] - 1, self.current[1])
        elif (cell_state == 2): # try up
            next_step = (self.current[0], self.current[1] - 1)
        elif (cell_state == 3): # try down
            next_step = (self.current[0], self.current[1] + 1)
        else:
            print("something went wrong / unsolvable")
        # print(self.path)
        # move into the next square if it's open
        if self._valid_next_step(next_step):
            self.path.append(self.current)
            self.current = next_step
        else:
            self.step() # move again if the last step failed
            pass
        

    def draw(self, surface, scale, offset):
        '''
        draw the solving process on the maze
        '''
        line_path = [(x * scale[0] + offset[0], y * scale[1] + offset[1]) for x, y in self.path]
        line_path.append((self.current[0] * scale[0] + offset[0], self.current[1] * scale[1] + offset[1]))
        pygame.draw.lines(surface, (0, 0, 0), False, line_path, 3)
