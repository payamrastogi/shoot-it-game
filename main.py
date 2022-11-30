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
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    screen.blit(bgs[level - 1], (0, 0))
    screen.blit(banners[level - 1], (0, HEIGHT - 200))

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

