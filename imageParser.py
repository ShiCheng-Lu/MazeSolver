import pygame
import copy


def almostWhite(colour):
    for i in range(3):
        if (colour[i] >= 128):
            return True
    return False


def enlarge_blacks(image):
    width, height = image.get_size()
    new_image = image.copy()
    for x in range(width):
        for y in range(height):
            if not almostWhite(image.get_at((x, y))):
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_image.set_at((x + dx, y + dy), (0, 0, 0))
    return new_image


def select_area(image, screen):
    '''
    display the image and let the user select an
    area of the image that would be the maze
    '''
    done = False
    defined = False
    while not done:
        new_image = image.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (pygame.mouse.get_pressed()[0]):
                    x1 = pygame.mouse.get_pos()[0]
                    y1 = pygame.mouse.get_pos()[1]
                    defined = True

        if (defined):
            if (pygame.mouse.get_pressed()[0]):
                x2 = pygame.mouse.get_pos()[0]
                y2 = pygame.mouse.get_pos()[1]

            left = min(x1, x2)
            top = min(y1, y2)

            width = abs(x1 - x2)
            height = abs(y1 - y2)

            maze_area = pygame.Rect(left, top, width, height)

            pygame.draw.rect(new_image, (0, 255, 0), maze_area, 1)
        screen.blit(new_image, (0, 0))
        pygame.display.flip()

    if (defined):
        return image.subsurface((left, top, width, height))
    else:
        return image


def shrink_area(image):
    '''
    reduce the image area so that the edges of the image
    is the edges of the maze
    blacks are the walls; whites are the open path
    '''
    width, height = image.get_size()
    min_x, min_y = width, height
    max_x, max_y = 0, 0

    for x in range(width):
        for y in range(height):
            if not almostWhite(image.get_at((x, y))):
                if (x < min_x):
                    min_x = x
                if (x > max_x):
                    max_x = x

                if (y < min_y):
                    min_y = y
                if (y > max_y):
                    max_y = y
    # return a image of the maze cropped to the maze area only
    return image.subsurface((min_x, min_y, max_x - min_x, max_y - min_y))

def cell_dimensions(image):
    '''
    return the dimensions of the maze, how many cells in total per side
    '''
    width, height = image.get_size()
    cell_count = 0
    on_line = False
    for i in range(min(width, height)):
        if on_line and almostWhite(image.get_at((i, i))):
            cell_count += 1
            on_line = False
        if not on_line and not almostWhite(image.get_at((i, i))):
            cell_count += 1
            on_line = True
    if (width < height):
        return cell_count, (int) (cell_count * height / width)
    else:
        return (int) (cell_count * width / height), cell_count

def normalize(image, xSize, ySize):
    '''

    '''
    # find the side length
    side_x, side_y = 0, 0
    width, height = image.get_size()
    
    # get the side lengths at x = 1, and y = 1

    ySample = 0
    for y in range(xSize, height, 2 * height // ySize):
        if not almostWhite(image.get_at((0, y))):
            ySample = y
            break
    for x in range(width):
        if almostWhite(image.get_at((x, ySample))):
            side_x = x
            break
    

    xSample = 0
    for x in range(xSize, width, 2 * width // xSize):
        if not almostWhite(image.get_at((x, 0))):
            xSample = x
            break
    for y in range(height):
        if almostWhite(image.get_at((xSample, y))):
            side_y = y
            break

    delta_x = side_x // 2
    delta_y = side_y // 2
    return image.subsurface((delta_x, delta_y, width - side_x + 2, height - side_y + 2))

def get_maze_data(image, width, height):
    '''
    return a maze data structure from a image,
    width and height are the number of cells in each dimension
    '''
    wSize = (image.get_size()[0] - 1) / (width - 1)
    hSize = (image.get_size()[1] - 1) / (height - 1)

    data = []
    for x in range(width):
        col = []
        for y in range(height):
            px = (int) (x * wSize)
            py = (int) (y * hSize)
            pixel = image.get_at((px, py))
            col.append(not almostWhite(pixel))
        data.append(col)
    return data


# def load_image:


#     return data
