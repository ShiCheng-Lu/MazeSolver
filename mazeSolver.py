class MazeSolver:

    def __init__(self, maze):
        self.maze = maze
        self.width = len(maze)
        self.height = len(maze[0])

        self.exits = []
        self._find_exits()

        self.start = self.exits[0]
        self.end = self.exits[-1]
        self.path = [self.start]
        self.complete = False

    def _find_exits(self):
        '''
        find the start point and end point of the maze
        start and ends are any points that are on the
        edge and open

        if more than one exit exists, start is always the highest
        exist, and end is always the lowest exist
        '''
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

    def _valid_loc(self, location):
        '''
        location is on the board (not out of range)
        '''
        if (location[0] < 0 or location[0] >= self.width):
            return False
        if (location[1] < 0 or location[1] >= self.height):
            return False
        return True
    
    def step(self):
        pass

    def draw(self, surface, scale, offset):
        pass