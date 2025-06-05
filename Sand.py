import pygame
import random
pygame.init()

scale = 10
grid_width = 80
grid_height = 100
screen_width = grid_width*scale
screen_height = grid_height*scale
screen = pygame.display.set_mode((screen_width, screen_height))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Create Sand (also fill a chunk in the center)
sand = []
for y in range(grid_height):
    sand.append([])
    for x in range(grid_width):
        if x > int(grid_width/2) and x < int(grid_width/2)+scale:
            sand[y].append(1.0)
        else:
            sand[y].append(0.0)

radius = 5
color_id = 1.0
def input():
    global color_id

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        color_id = 1
    elif keys[pygame.K_2]:
        color_id = 2
    elif keys[pygame.K_3]:
        color_id = 3

    frac = (1.0/float(random.randint(1, 1000)))
    print(frac)
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
        sand[y][x] = color_id+frac if sand[y][x] == 0 else sand[y][x]
    
    # Create Chunks
    elif pygame.mouse.get_pressed()[1]:
        sand[y][x] = color_id+frac if sand[y][x] == 0 else sand[y][x]
        # Prevent out of array bounds when - or + index
        # Fill
        if (y > radius and y < grid_height-radius) and (x > radius and x < grid_width-radius):
            for i in range(radius):
                for j in range(radius):
                    sand[y+i][x+j] = color_id+frac if sand[y+i][x+j] == 0 else sand[y+i][x+j]
                    sand[y+i][x-j] = color_id+frac if sand[y+i][x-j] == 0 else sand[y+i][x-j]
                    sand[y-i][x+j] = color_id+frac if sand[y-i][x+j] == 0 else sand[y-i][x+j]
                    sand[y-i][x-j] = color_id+frac if sand[y-i][x-j] == 0 else sand[y-i][x-j]
    # Delete
    elif pygame.mouse.get_pressed()[2]:
        sand[y][x] = 0
        # Prevent out of array bounds when - or + index
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
            sand_color_id = sand[y][x]
            if sand[y][x] > 0 and sand[y+1][x] == 0:
                sand[y][x] = 0
                sand[y+1][x] = sand_color_id
            #, otherwise we know below us contains sand, 
            #, but move on the x if random value (left or right) below us is empty, move
            elif sand[y][x] > 0:
                # Prevent out of array bounds when - or + index
                if x > 0 and x < grid_width-2:
                    dir = random.randint(-1, 1)
                    if sand[y+1][x+dir] == 0:
                        sand[y][x] = 0
                        sand[y+1][x+dir] = sand_color_id

def draw():
    screen.fill(WHITE)
    for y in range(grid_height):
        for x in range(grid_width):
            sand_color_id = sand[y][x]
            color = None
            if sand_color_id > 0:
                
                # Determine gradient
                gradient = 1000.0 * (float(sand_color_id) - float(int(sand_color_id)) )
                if gradient <= 0.00:
                    gradient = 1
                c = (255/gradient) 
                if c > 255:
                    c = 255
                # Limit c from going too dark
                elif c < 200:
                    c = 200
                
                # Determine color
                if int(sand_color_id) == 1:
                    # color = (c_x, c_y, 100)
                    color = (c, 0, 0)
                elif int(sand_color_id) == 2:
                    color = (0, c, 0)
                elif int(sand_color_id) == 3:
                    color = (0, 0, c)
                else:
                    color = (c, c, 100)

                pygame.draw.rect(screen, color, (x*scale, y*scale, scale, scale)) #, 1)
                pygame.draw.rect(screen, BLACK, (x*scale, y*scale, scale, scale), 1)
            else:
                pass
                # pygame.draw.rect(screen, (128, 128, 128), (x*scale, y*scale, scale, scale), 1)
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