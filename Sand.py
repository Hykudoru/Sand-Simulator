import pygame
import random
pygame.init()

font = pygame.font.SysFont('Arial', 16)
pygame.mouse.set_visible(False)

class Settings:
    stickySand = False
    display_ui_controls = False
    fg_fill = True

settings = Settings()
scale = 10
grid_width = 80
grid_height = 80
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

def determine_color(id, c = 255):
    if int(id) == 1:
        # color = (c_x, c_y, 100)
        color = (c, 0, 0)
    elif int(id) == 2:
        color = (0, c, 0)
    elif int(id) == 3:
        color = (0, 0, c)
    elif int(id) == 4:
        color = (c, c, 0)
    elif int(id) == 5:
        color = (c, 0, c)
    elif int(id) == 6:
        color = (0, c, c)
    elif int(id) == 7:
        color = (c, c, c)
    else:
        color = (c, c, 100)
    return color

def input():
    global color_id

    # Controls
    keys = pygame.key.get_just_pressed()
    if keys[pygame.K_ESCAPE]:
        settings.display_ui_controls = not settings.display_ui_controls
    if keys[pygame.K_SPACE]:
        settings.stickySand = not settings.stickySand
    if keys[pygame.K_f]:
        settings.fg_fill = not settings.fg_fill
    if keys[pygame.K_1]:
        color_id = 1
    elif keys[pygame.K_2]:
        color_id = 2
    elif keys[pygame.K_3]:
        color_id = 3
    elif keys[pygame.K_4]:
        color_id = 4
    elif keys[pygame.K_5]:
        color_id = 5
    elif keys[pygame.K_6]:
        color_id = 6
    elif keys[pygame.K_7]:
        color_id = 7
        
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
    
    color_frac = (1.0/float(random.randint(1, 1000)))

    # Create
    if pygame.mouse.get_pressed()[0]:
        sand[y][x] = color_id+color_frac if sand[y][x] == 0 else sand[y][x]
        # Prevent out of array bounds when - or + index
        # Fill
        for i in range(radius):
            for j in range(radius):
                if x-j < 0 or y-i < 0:
                    continue
                try: sand[y+i][x+j] = color_id+color_frac if sand[y+i][x+j] == 0 else sand[y+i][x+j]
                except: pass
                try: sand[y+i][x-j] = color_id+color_frac if sand[y+i][x-j] == 0 else sand[y+i][x-j]
                except: pass
                try: sand[y-i][x+j] = color_id+color_frac if sand[y-i][x+j] == 0 else sand[y-i][x+j]
                except: pass
                try: sand[y-i][x-j] = color_id+color_frac if sand[y-i][x-j] == 0 else sand[y-i][x-j]
                except: pass
    # Delete
    elif pygame.mouse.get_pressed()[2]:
        sand[y][x] = 0
        # Prevent out of array bounds when - or + index
        for i in range(radius):
            for j in range(radius):
                if x-j < 0 or y-i < 0:
                    continue
                try: sand[y+i][x+j] = 0 
                except: pass
                try: sand[y+i][x-j] = 0
                except: pass
                try: sand[y-i][x+j] = 0
                except: pass
                try: sand[y-i][x-j] = 0
                except: pass
def update():
    # Sand Grid Movement
    for y in range(grid_height-2, -1, -1):
        for x in range(grid_width):
            # If point has sand but empty below, fall 
            sand_color_id = sand[y][x]
            if sand[y][x] > 0 and sand[y+1][x] == 0:
                sand[y][x] = 0
                sand[y+1][x] = sand_color_id
            #, otherwise we know below us contains sand, 
            #, but move on the x if random value (left or right) below us is empty, move
            if not settings.stickySand:
                if sand[y][x] > 0:
                    # Prevent out of array bounds when - or + index
                    if x > 0 and x < grid_width-2:
                        dir = random.randint(-1, 1)
                        if sand[y+1][x+dir] == 0:
                            sand[y][x] = 0
                            sand[y+1][x+dir] = sand_color_id

def drawUI():
    offset_amt = 25
    text_temp = "Press ESC to hide controls"
    screen.blit(font.render(text_temp, True, WHITE), ((screen_width/2)-16-len(text_temp), 20))
    text_offset = offset_amt
    screen.blit(font.render(f"- MOUSE LEFT: Place sand", True, WHITE), (20, text_offset))
    text_offset += offset_amt
    screen.blit(font.render(f"- MOUSE RIGHT: Remove sand", True, WHITE), (20, text_offset))
    text_offset += offset_amt
    screen.blit(font.render(f"- MOUSE SCROLL WHEEL: Adjust cursor size", True, WHITE), (20, text_offset))
    text_offset += offset_amt
    screen.blit(font.render(f"- SPACEBAR: Toggle dry/wet sand", True, WHITE), (20, text_offset))
    text_offset += offset_amt
    screen.blit(font.render(f"- Press F: Toggle x-ray mode ", True, WHITE), (20, text_offset))
    text_offset += offset_amt
    screen.blit(font.render(f"- Press Nums 1 - 7 (to change sand color)", True, WHITE), (20, text_offset))

def draw():
    screen.fill(BLACK)
    
    if settings.display_ui_controls:
        drawUI()
    else:
        screen.blit(font.render(f"Press ESC for controls", True, WHITE), (20, 20))

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
                color = determine_color(sand_color_id, c)
                if settings.fg_fill:
                    pygame.draw.rect(screen, color, (x*scale, y*scale, scale, scale))
                else:
                    pygame.draw.rect(screen, color, (x*scale, y*scale, scale, scale), 1)
            
            # Mouse Marker Outline        
            (x_mouse, y_mouse) = pygame.mouse.get_pos()
            color = determine_color(color_id)
            if radius == 1:
                pygame.draw.rect(screen, color, (x_mouse-(scale), y_mouse-(scale), scale*radius, scale*radius), 1)
            else:
                pygame.draw.rect(screen, color, (x_mouse-(radius*scale), y_mouse-(radius*scale), scale*2*radius, scale*2*radius), 1)
            
    pygame.display.flip()

# The game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            radius += event.y
            if (radius <= 0):
                radius = 1
    input()
    update()
    draw()
    # Control the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()