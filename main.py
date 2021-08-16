import pygame
from PIL import Image
from mazeSolverDeadend import *
from imageParser import *
import sys

image_file = "maze2.png"
speed = 60 # step per second

pygame.init()

def init_display_surface():
    global image_file
    if len(sys.argv) > 1:
        imageFile = sys.argv[1]
    elif image_file != None:
        imageFile = image_file
    else:
        imageFile = input("maze file: ")

    image = pygame.image.load(imageFile)
    image = pygame.transform.scale2x(image)

    screen = pygame.display.set_mode(image.get_size())
    pygame.display.set_caption("Maze")
    
    return image, screen


def get_data_from_image(image, screen):
    # get the maze to it's smallest size
    image = shrink_area(select_area(image, screen))
    image = enlarge_blacks(image)
    dimensions = cell_dimensions(image)
    # shrink the maze image more to center sample locations
    image = normalize(image, *dimensions)
    return get_maze_data(image, *dimensions), image, dimensions

def plot_availiable_paths(surface, data, dimensions):
    width, height = dimensions
    wSize = (surface.get_size()[0] - 1) / (width - 1)
    hSize = (surface.get_size()[1] - 1) / (height - 1)

    for x in range(len(data)):
        for y in range(len(data[0])):
            if (data[x][y]):
                pygame.draw.circle(surface, (0, 0, 0), (x * wSize, y * hSize), 1)
            else:
                pygame.draw.circle(surface, (255, 255, 255), (x * wSize, y * hSize), 1)

def show_maze_solve(surface, maze, dimensions):
    clock = pygame.time.Clock()

    width, height = dimensions
    wSize = (surface.get_size()[0] - 1) / (width - 1)
    hSize = (surface.get_size()[1] - 1) / (height - 1)

    done = False
    while not done:
        path = surface.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
        maze.step()

        maze.draw(path, (wSize, hSize), (0, 0))

        screen.blit(path, (0, 0))
        pygame.display.flip()
        clock.tick(speed)

if __name__ == "__main__":
    image, screen = init_display_surface()

    data, image, dimensions = get_data_from_image(image, screen)
    screen = pygame.display.set_mode(image.get_size())

    # plot_availiable_paths(image, data, dimensions)
    # create the maze class with the path data
    maze = MazeSolver(data)
    show_maze_solve(image, maze, dimensions)
