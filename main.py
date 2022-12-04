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

level = 0 # level 0 is Main Menu
points = 0
best_freeplay= 0
best_ammo = 0
best_time =0

shot = False
total_shots = 0
# 0 = freeplay , 1 - accuracy, 2 - timed
mode = 0
ammo = 0
time_passed = 0
time_remaining = 0
counter = 1
menu = True
game_over = False
pause = False



# load images
menu_img = pygame.image.load(f'assets/menus/mainMenu.png')
game_over_img = pygame.image.load(f'assets/menus/gameOver.png')
pause_img = pygame.image.load(f'assets/menus/pause.png')

for i in range(1, 4):
    bgs.append(pygame.image.load(f'assets/bgs/{i}.png'))
    banners.append(pygame.image.load(f'assets/banners/{i}.png'))
    guns.append(pygame.image.load(f'assets/guns/{i}.png'))
    if i<3:
        for j in range(1, 4):
            target_images[i-1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{i}/{j}.png'), (120 - (j*18), 80 - (j*12))))
    else:
        for j in range(1, 5):
            target_images[i-1].append(pygame.transform.scale(
                pygame.image.load(f'assets/targets/{i}/{j}.png'), (120 - (j*18), 80 - (j*12))))

# ----
def draw_score():
    points_text = font.render(f'Points: {points}', True, 'black')
    screen.blit(points_text, (320, 660))
    shots_text = font.render(f'Total Shots: {total_shots}', True, 'black')
    screen.blit(shots_text, (320, 687))
    time_text= font.render(f'Time Elapsed: {time_passed}', True, 'black')
    screen.blit(time_text, (320, 714))
    if mode == 0:
        mode_text = font.render(f'Freeplay!', True, 'black')
    if mode == 1:
        mode_text = font.render(f'Ammo Remaining: {ammo}', True, 'black')
    if mode == 2:
        mode_text = font.render(f'Time Remaining: {time_remaining}', True, 'black')
    screen.blit(mode_text, (320, 741))
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

# -----
# move target objects
def move_level(coords):
    if level == 1 or level == 2:
        # number of enemy levels
        max_val = 3
    else:
        max_val = 4
    for i in range(max_val):
        for j in range(len(coords[i])):
            my_coords = coords[i][j]
            # if you have gone off-screen to the left, move to the right
            if my_coords[0] < -150:
                coords[i][j] = (WIDTH, my_coords[1])
            else:
                coords[i][j] = (my_coords[0] - 2**i, my_coords[1])
    return coords
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


# check if the target rects has been hit
def check_shot(targets, coords):
    global points
    mouse_pos = pygame.mouse.get_pos()
    # i tier of the target
    for i in range(len(targets)):
        for j in range(len(targets[i])):
            if targets[i][j].collidepoint(mouse_pos):
                coords[i].pop(j)
                # tier score 10 20 50 100
                points += 10 + 10 * (i**2)
                # add sounds for enemy hit
    return coords

# ---
# draw menu
def draw_menu():
    global game_over, pause
    game_over = False
    pause = False
    screen.blit(menu_img, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    freeplay_button = pygame.draw.rect(screen, 'green', [170, 524, 260, 100], 3)
    screen.blit(font.render(f'{best_freeplay}', True, 'black'), (340, 580))
    ammo_button = pygame.rect.Rect((475, 524), (260, 100))
    screen.blit(font.render(f'{best_ammo}', True, 'black'), (650, 580))
    timed_button = pygame.rect.Rect((170, 661), (260, 100))
    screen.blit(font.render(f'{best_time}', True, 'black'), (350, 710))
    reset_button = pygame.rect.Rect((475, 661), (260, 100))

def draw_game_over():
    pass

def draw_pause():
    pass

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
        three_coords[i].append((WIDTH // (my_list[i]) * j, 300 - (i * 100) + 30 * (j % 2)))

# ------
run = True
while run:
    timer.tick(fps)
    if level != 0:
        if counter < 60:
            counter += 1
        else:
            counter = 1
            time_passed+=1
            if mode == 2:
                time_remaining -= 1

    screen.fill('black')
    screen.blit(bgs[level - 1], (0, 0))
    screen.blit(banners[level - 1], (0, HEIGHT - 200))
    if menu:
        level = 0
        draw_menu()
    if game_over:
        level = 0
        draw_game_over()
    if pause:
        level = 0
        draw_pause()


    if level == 1:
        target_boxes = draw_level(one_coords)
        one_coords = move_level(one_coords)
        if shot:
            one_coords = check_shot(target_boxes, one_coords)
            shot=False
    elif level == 2:
        target_boxes = draw_level(two_coords)
        two_coords = move_level(two_coords)
        if shot:
            two_coords = check_shot(target_boxes, two_coords)
            shot = False
    elif level == 3:
        target_boxes = draw_level(three_coords)
        three_coords = move_level(three_coords)
        if shot:
            three_coords = check_shot(target_boxes, three_coords)
            # prevent hold down the mouse click and drag it all over the screen
            shot = False
    #draw gun
    if level > 0:
        draw_gun()
        # after the blit.banner
        draw_score()
    # to get out of the infinite loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # if the mouse button is pressed, and it's the left button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pygame.mouse.get_pos()
            if( 0 < mouse_position[0] < WIDTH ) and (0 < mouse_position[1] < HEIGHT - 200):
                shot = True
                total_shots += 1
                if mode == 1:
                    ammo -= 1

    if level > 0:
        if target_boxes == [[], [], []] and level < 3:
            level += 1
    # take everything and display it on the screen
    pygame.display.flip()
# close the program
pygame.quit()

# ---

