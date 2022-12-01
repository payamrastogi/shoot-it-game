import pygame
import math

pygame.init()
# Game Setup/Config
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('assets/font/myFont.ttf', 32)
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bgs = []
banners = []
guns = []
target_images = [[], [], []]
# we want 10 big red bird, 5 middle size birds, 3 small birds
targets = {1: [10, 5, 3],
           2: [12, 8, 5],
           3: [15, 12, 8, 3]}

level = 2 # level 0 is Main Menu

for i in range(1, 4):
    bgs.append(pygame.image.load(f'assets/bgs/{i}.png'))
    banners.append(pygame.image.load(f'assets/banners/{i}.png'))
    guns.append(pygame.image.load(f'assets/guns/{i}.png'))
# ---
# rotate the gun and point it in the direction of the mouse cursor
def draw_gun():
    mouse_pos = pygame.mouse.get_pos()
    gun_point = (WIDTH/2, HEIGHT - 200)
    lasers = ['red', 'purple', 'green']
    clicks = pygame.mouse.get_pressed()
    # to prevent divide by zero
    if mouse_pos[0] != gun_point[0]:
        # (y2 - y2)/(x2-x1)
        slope = (mouse_pos[1] - gun_point[1])/(mouse_pos[0] - gun_point[0])
    else:
        slope = -100000
    # inverse tangent of the slope of the line would give the angle
    angle = math.atan(slope)
    rotation = math.degrees(angle)

    # gun orientation
    if mouse_pos[0] < WIDTH/2:
        gun = pygame.transform.flip(guns[level - 1], True, False)
        # shoot only if the mouse is in the shooting area
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(gun, 90 - rotation), (WIDTH/2 - 90 , HEIGHT - 250))
            if clicks[0]:
                pygame.draw.circle(screen, lasers[level-1], mouse_pos, 5)
    else:
        gun = guns[level - 1]
        if mouse_pos[1] < 600:
            screen.blit(pygame.transform.rotate(gun, 270 - rotation), (WIDTH / 2 - 30, HEIGHT - 250))
            if clicks[0]:
                pygame.draw.circle(screen, lasers[level - 1], mouse_pos, 5)

# -------
# coords a list of coordinates for all the enemies
def draw_level(coords):
    if level == 1 or level == 2:
        # hit boxes inside the images
        # required for collision detection
        target_rects = [[], [], []]
    else:
        target_rects = [[], [], [], []]
    for i in range(len(coords)):
        for j in range(len(coords[i])):
            # images have blank space on the side
            # make images smaller as the level grow
            target_rects[i].append(pygame.rect.Rect((coords[i][j][0] + 20, coords[i][j][1]),
                                                    (60 - i*12, 60 - i*12)))
            screen.blit(target_images[level-1][i], coords[i][j])
    return target_rects

# initialize enemy coordinates
one_coords = [[], [], []]
two_coords = [[], [], []]
three_coords = [[], [], [], []]

for i in range(3):
    my_list = targets[1]
    # create random coords
    # for j in range (10)
    for j in range(my_list[i]):
        # floor division
        one_coords[i].append((WIDTH//(my_list[i]) * j, 300 - (i * 150) + 30*(j % 2)))

for i in range(3):
    my_list = targets[2]
    # create random coords
    for j in range(my_list[i]):
        # floor division
        two_coords[i].append((WIDTH // (my_list[i]) * j, 300 - (i * 150) + 30 * (j % 2)))

for i in range(4):
    my_list = targets[3]
    # create random coords
    for j in range(my_list[i]):
        # floor division
        # tuple (x, y) coordinate
        three_coords[i].append((WIDTH // (my_list[i]) * j, 300 - (i * 150) + 30 * (j % 2)))

# ------
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    screen.blit(bgs[level - 1], (0, 0))
    screen.blit(banners[level - 1], (0, HEIGHT - 200))
    if level == 1:
        draw_level(one_coords)
    elif level == 2:
        draw_level(two_coords)
    elif level == 3:
        draw_level(three_coords)
    #draw gun
    if level > 0:
        draw_gun()

    # to get out of the infinite loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # take everything and display it on the screen
    pygame.display.flip()
# close the program
pygame.quit()

# ---

