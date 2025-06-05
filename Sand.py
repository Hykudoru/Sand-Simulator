import pygame
import random
pygame.init()

scale = 10
grid_width = 50
grid_height = 100
screen_width = grid_width*scale
screen_height = grid_height*scale
screen = pygame.display.set_mode((screen_width, screen_height))

# Create Sand (also fill a chunk in the center)
sand = []
for y in range(grid_height):
    sand.append([])
    for x in range(grid_width):
        if x > int(grid_width/2) and x < int(grid_width/2)+scale:
            sand[y].append(1)
        else:
            sand[y].append(0)

radius = 5
def input():
    (x_mouse, y_mouse) = pygame.mouse.get_pos()
    x = int(x_mouse/scale)
    y = int(y_mouse/scale)
    # Return if out of bounds
    if x < 0 or x > grid_width-1:
        return
    if y < 0 or y > grid_height-1:
        return
    if sand[y][x] < 0:
        return
    
    # Create
    if pygame.mouse.get_pressed()[0]:
        sand[y][x] = 1
    
    # Create Chunks
    if pygame.mouse.get_pressed()[1]:
        sand[y][x] = 1
        # Prevent out of array bounds when - or + index
        # Fill
        if (y > radius and y < grid_height-radius) and (x > radius and x < grid_width-radius):
            for i in range(radius):
                for j in range(radius):
                    sand[y+i][x+j] = 1
                    sand[y+i][x-j] = 1
                    sand[y-i][x+j] = 1
                    sand[y-i][x-j] = 1
    # Delete
    elif pygame.mouse.get_pressed()[2]:
        sand[y][x] = 0
        # Prevent out of array bounds when - or + index
        # Fill
        if (y > radius and y < grid_height-radius) and (x > radius and x < grid_width-radius):
            for i in range(radius):
                for j in range(radius):
                    sand[y+i][x+j] = 0
                    sand[y+i][x-j] = 0
                    sand[y-i][x+j] = 0
                    sand[y-i][x-j] = 0

def update():
    for y in range(grid_height-2, -1, -1):
        for x in range(grid_width):
            # If point has sand but empty below, fall 
            if sand[y][x] == 1 and sand[y+1][x] == 0:
                sand[y][x] = 0
                sand[y+1][x] = 1
            #, otherwise we know below us contains sand, 
            #, but move on the x if random value (left or right) below us is empty, move
            elif sand[y][x] == 1:
                # Prevent out of array bounds when - or + index
                if x > 0 and x < grid_width-2:
                    dir = random.randint(-1, 1)
                    if sand[y+1][x+dir] == 0:
                        sand[y][x] = 0
                        sand[y+1][x+dir] = 1

def draw():
    screen.fill((255,255,255))
    for y in range(grid_height):
        for x in range(grid_width):
            if sand[y][x] == 1:
                r = y
                if y > 240:
                    r = 240
                pygame.draw.rect(screen, (240-r, 0, 0), (x*scale, y*scale, scale, scale))#, 1)
            # else:
            #     pygame.draw.rect(screen, (128, 128, 128), (x*scale, y*scale, pixel_size*scale, pixel_size*scale), 1)
    pygame.display.flip()

# The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    input()
    update()
    draw()
    # Control the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()