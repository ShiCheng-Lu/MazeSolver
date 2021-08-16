import pygame

class MazeSolverShortest:
    def __init__(self, maze):
        self.maze = maze
        self.width = len(maze)
        self.height = len(maze[0])

        self._find_start_end()

        self.start = self.exits[0]
        self.end = self.exits[-1]

        self.complete = False

        self.max_dist = self.width * self.height
        self.shortest = [[self.max_dist for y in range(self.height)] for x in range(self.width)]

        self.shortest[self.start[0]][self.start[1]] = 0
        self.path = [self.end, self.end]
        self.current_dist = 0
    
    def _find_start_end(self):
        self.exits = []
        for x in range(1, self.width - 1):
            if (not self.maze[x][0]):
                self.exits.append((x, 0))
            if (not self.maze[x][self.height - 1]):
                self.exits.append((x, self.height - 1))
        
        for y in range(1, self.height - 1):
            if (not self.maze[0][y]):
                self.exits.append((0, y))
            if (not self.maze[self.width - 1][y]):
                self.exits.append((self.width - 1, y))
        return

    def _can_step(self, location):
        return not self.maze[location[0]][location[1]]
    
    def _in_path(self, location):
        return location in self.path
    
    def _valid_loc(self, location):
        if (location[0] < 0 or location[0] >= self.width):
            return False
        if (location[1] < 0 or location[1] >= self.height):
            return False
        return True
    
    def _update_neighbour(self, x, y, dist):
        min_coord = (0, 0)
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            fx = x + dx
            fy = y + dy
            if fx < 0 or fx >= self.width:
                continue
            elif fy < 0 or fy >= self.height:
                continue
            elif self.maze[fx][fy]:
                continue
            elif self.shortest[fx][fy] > dist:
                self.shortest[fx][fy] = dist + 1
        return

    def _least_neighbour(self, x, y):
        least = self.max_dist
        coord = (0, 0)
        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            fx = x + dx
            fy = y + dy
            if fx < 0 or fx >= self.width:
                continue
            elif fy < 0 or fy >= self.height:
                continue
            elif self.shortest[x][y] <= least:
                coord = (fx, fy)
                least = self.shortest[fx][fy]
        return coord

    def step(self):
        if self.path[-1] == self.start:
            return

        if self.complete:
            x, y = self.path[-1]
            self.path.append(self._least_neighbour(x, y))
            return

        for x in range(self.width):
            for y in range(self.height):
                if self.shortest[x][y] == self.current_dist:
                    self._update_neighbour(x, y, self.current_dist)
        self.current_dist += 1
        
        if self.shortest[self.end[0]][self.end[1]] != self.max_dist:
            self.complete = True

    def draw(self, surface, scale, offset):
        dot_size = 3
        if self.complete:
            dot_size = 1

        for x in range(self.width):
            for y in range(self.height):
                if self.shortest[x][y] != self.max_dist:
                    display_x = x * scale[0] + offset[0]
                    display_y = y * scale[1] + offset[1]
                    pygame.draw.circle(surface, (0, 0, 0), (display_x, display_y), dot_size)
        if self.complete:
            line_path = [(x * scale[0] + offset[0], y * scale[1] + offset[1]) for x, y in self.path]
            pygame.draw.lines(surface, (0, 0, 0), False, line_path, 3)
