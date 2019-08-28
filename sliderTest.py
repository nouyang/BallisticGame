import pygame as pg
from pygame.locals import *
from sys import exit

pg.init()

WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT), 0, 32)
color = [127, 127, 127]

# Creates an image with smooth gradients
def createScales(height):
    redScaleSurface = pg.surface.Surface((WIDTH, height))
    greenScaleSurface = pg.surface.Surface((WIDTH,height))
    blueScaleSurface = pg.surface.Surface((WIDTH,height))
    for x in range(WIDTH):
        c =int((x/(WIDTH-1.))*255.)
        red = (c, 0, 0)
        green = (0, c, 0)
        blue = (0, 0, c)
        line_rect = Rect(x, 0, 1, height)
        pg.draw.rect(redScaleSurface, red, line_rect)
        pg.draw.rect(greenScaleSurface, green, line_rect)
        pg.draw.rect(blueScaleSurface, blue, line_rect)
    return redScaleSurface, greenScaleSurface, blueScaleSurface

redScale, greenScale, blueScale = createScales(80)

while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.fill((0, 0, 0))

    # Draw the scales to the screen
    screen.blit(redScale, (0, 00))
    screen.blit(greenScale, (0, 80))
    screen.blit(blueScale, (0, 160))

    x, y = pg.mouse.get_pos()

    # If the mouse was pressed on one of the sliders, adjust the color component
    if pg.mouse.get_pressed()[0]:
        for component in range(3):
            if y > component*80 and y < (component+1)*80:
                color[component] = int((x/(WIDTH-1.))*255.)
        pg.display.set_caption("PyGame Color Test - " + str(tuple(color)))

    # Draw a circle for each slider to represent the curret setting
    for component in range(3):
        pos = ( int((color[component]/255.)*(WIDTH-1)), component*80+40 )
        pg.draw.circle(screen, (255, 255, 255), pos, 20)

    pg.draw.rect(screen, tuple(color), (0, 240, WIDTH, HEIGHT/2))

    pg.display.update()
