import pygame
from PIL import Image
from mazeSolverDeadend import *
from mazeSolverRecursive import *
from mazeSolverShortest import *

from imageParser import *
import sys

image_file = "maze2.png"
speed = 240 # step per second
strategy = MazeSolverDeadend

pygame.init()

def init_display_surface():
    '''
    open the maze file and create a screen
    based in the image size
    '''
    global image_file
    if len(sys.argv) > 1:
        imageFile = sys.argv[1]
    elif image_file != None:
        imageFile = image_file
    else:
        imageFile = input("maze file: ")

    image = pygame.image.load(imageFile)
    width, height = image.get_size()
    while (width < 500 and height < 300):
        image = pygame.transform.scale2x(image)
        width, height = image.get_size()

    screen = pygame.display.set_mode(image.get_size())
    pygame.display.set_caption("Maze")
    
    return image, screen


def get_data_from_image(image, screen):
    '''
    retrieve the maze data from the image
    '''
    # get the maze to it's smallest size
    image = shrink_area(select_area(image, screen))
    image = enlarge_blacks(image)
    dimensions = cell_dimensions(image)
    # shrink the maze image more to center sample locations
    image = normalize(image, *dimensions)
    return get_maze_data(image, *dimensions), image, dimensions

def plot_availiable_paths(surface, data, dimensions):
    '''
    draw a white dot for everywhere that the program decide has a wall
    draw a black dot for everywhere that the program decide is open

    for debug only
    '''
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
    '''
    display the process of the maze solve
    '''
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
    maze = strategy(data)
    show_maze_solve(image, maze, dimensions)
