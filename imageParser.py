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
        return cell_count, cell_count * height // width
    else:
        return cell_count * width // height, cell_count

def normalize(image, xSize, ySize):
    # find the side length
    side_x, side_y = 0, 0
    width, height = image.get_size()
    
    # get the side lengths at x = 1, and y = 1
    for x in range(height):
        if almostWhite(image.get_at((x, height // ySize))):
            side_x = x
            break
    
    for y in range(height):
        if almostWhite(image.get_at((width // xSize, y))):
            side_y = y
            break

    delta_x = side_x // 2
    delta_y = side_y // 2
    return image.subsurface((delta_x, delta_y, width - delta_x, height - delta_y))

def get_maze_data(image, width, height):
    wSize = (image.get_size()[0] - 1) / (width - 1)
    hSize = (image.get_size()[1] - 1) / (height - 1)

    data = []
    for y in range(height):
        row = []
        for x in range(width):
            px = (int) (x * wSize)
            py = (int) (y * hSize)
            pixel = image.get_at((px, py))
            row.append(almostWhite(pixel))
        data.append(row)
    return data


# def load_image:


#     return data
