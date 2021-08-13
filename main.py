import pygame
from PIL import Image
from algorithm import *
from imageParser import *

pygame.init()

imageFile = "maze.png"

# initialze display size - 2x image size
image = pygame.image.load(imageFile)
image = pygame.transform.scale2x(image)
x, y = image.get_size()

screen = pygame.display.set_mode(image.get_size())
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()


image = shrink_area(select_area(image, screen))
dimensions = cell_dimensions(image)
image = normalize(image, *dimensions)

screen = pygame.display.set_mode(image.get_size())

screen.blit(image, (5, 5))
pygame.draw.rect(screen, (140, 140, 140), pygame.Rect(5, 5, 900, 900), 1)

print(dimensions)

data = get_maze_data(image, *dimensions)

width, height = cell_dimensions(image)
wSize = (image.get_size()[0] - 1) / (width - 1)
hSize = (image.get_size()[1] - 1) / (height - 1)

for x in range(len(data)):
    for y in range(len(data[0])):
        if (data[x][y]):
            pygame.draw.circle(image, (0, 0, 0), (x * wSize, y * hSize), 1)
        else:
            pygame.draw.circle(image, (255, 255, 255), (x * wSize, y * hSize), 1)

# print(len(data))

maze = MazeSolver(data)

done = False
while not done:
    path = image.copy()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
    maze.step()

    maze.draw(path, (wSize, hSize), (0, 0))

    screen.blit(path, (0, 0))
    pygame.display.flip()
    clock.tick(240)
