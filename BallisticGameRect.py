import pygame, sys
from pygame.locals import *
from math import *

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

pygame.init()

FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((640, 720), 0, 32)
pygame.display.set_caption('Ballistic Game')

backgroundImg = pygame.image.load('images/background.png')
cannonBaseImg = pygame.image.load('images/cannonBase.png')
cannonImg = pygame.image.load('images/cannonTube.png')
ballImg = pygame.image.load('images/cannonBall_rect.png')

# positions of the cannon parts
cannonBasePos = (15,478)
cannonPos = (-5, 450)
ballPos = (22,478)

# make the cannon horizontal
cannonImg = pygame.transform.rotate(cannonImg, -15)

# set the default cannon angle
ang = 45
cannonMovImg = rot_center(cannonImg, ang)

# blit the images
DISPLAYSURF.blit(backgroundImg, (0,0))
DISPLAYSURF.blit(cannonMovImg, cannonPos  )
DISPLAYSURF.blit(ballImg, ballPos)
DISPLAYSURF.blit(cannonBaseImg, cannonBasePos)

# set the physical quantities
t = 0 # time
state = ballPos # space
v = (0, 0) # velocity
vm = 60 # initial speed
launched = False # ball shoted
v0 = (-99, -99)
time_f = 0
w = -45. # deg/ sec
theta = 0


WIDTH =200 
HEIGHT = 51
sliderVelocity =  pygame.surface.Surface((WIDTH, HEIGHT))
LOCX, LOCY = 0, 40

GOALX = 200


def createSlider():
    for x in range(WIDTH):
        # c = int((x/(WIDTH-1.))*255.)
        sliderColor = (200, 0, 0)
        line_rect = Rect(x, 0, 1, HEIGHT)
        pygame.draw.rect(sliderVelocity, sliderColor, line_rect)
    return sliderVelocity

sliderVel = createSlider()
sliderVelPos = 10

# the main game loop
while True:
    dt = fpsClock.tick(FPS) # dt = t_now - t_previous
    if launched:
        t = t + dt/50.0 # updated time #250 is a little more accurate  than 50
        theta = w * t
        a = (0.0, 10.0) # acceleration
        v =  (v0[0] + a[0]*t, v0[1] + a[1]*t) # velocity
        vm = sqrt(v[0]*v[0] + v[1]*v[1])
        s0 = ballPos # initial position
        state = (s0[0] + v0[0]*t + a[0]*t*t/2, s0[1] + v0[1]*t + a[1]*t*t/2)
        # if state[1] >= 486: # if hit the ground
        if state[0] >= GOALX: # if hit the board  
            time_f = t
            print('Time taken', time_f)
            print('Final angle', theta)
            vm = 60 # initial speed
            launched = False

    #  set informations to print
    font = pygame.font.Font(None, 30)
    text_w = font.render("w, theta = %.2f, %.2f" % (w, theta), 1, (10, 10, 10))
    text_w_pos = (300, 620)

    font = pygame.font.Font(None, 30)
    text_v0= font.render("v0= %.2f, %.2f" % v0, 1, (10, 10, 10))
    text_v0_pos = (300, 540)


    text_time= font.render("time_f= %.2f" % time_f, 1, (10, 10, 10))
    text_time_pos = (300, 580)


    text_ang = font.render("angle = %d" % ang, 1, (10, 10, 10))
    text_ang_pos = (300, 640)

    text_vm = font.render("vm = %.1f m/s" % vm, 1, (10, 10, 10))
    text_vm_pos = (0, 560)

    text_vx = font.render("vx = %.1f m/s" % v[0], 1, (10, 10, 10))
    text_vx_pos = (0, 580)

    text_vy = font.render("vy = %.1f m/s" % v[1], 1, (10, 10, 10))
    text_vy_pos = (0, 600)

    text_x = font.render("x = %.1f m" % state[0], 1, (10, 10, 10))
    text_x_pos = (0, 620)

    text_y = font.render("y = %.1f m" % state[1], 1, (10, 10, 10))
    text_y_pos = (0, 640)

    text_t = font.render("t = %.1f s" % t, 1, (10, 10, 10))
    text_t_pos = (0, 660)

    ballRot = pygame.transform.rotate(ballImg, theta)



    # blit the new scene
    DISPLAYSURF.blit(backgroundImg, (0,0))
    DISPLAYSURF.blit(cannonMovImg, cannonPos)
    DISPLAYSURF.blit(ballRot, state)
    DISPLAYSURF.blit(cannonBaseImg, cannonBasePos)
    DISPLAYSURF.blit(text_time, text_time_pos)
    DISPLAYSURF.blit(text_v0, text_v0_pos)
    DISPLAYSURF.blit(text_t, text_t_pos)
    DISPLAYSURF.blit(text_vx, text_vx_pos)
    DISPLAYSURF.blit(text_vy, text_vy_pos)
    DISPLAYSURF.blit(text_vm, text_vm_pos)
    DISPLAYSURF.blit(text_x, text_x_pos)
    DISPLAYSURF.blit(text_y, text_y_pos)
    DISPLAYSURF.blit(text_ang, text_ang_pos)
    DISPLAYSURF.blit(text_w, text_w_pos)
    # blit the velocity slider
    DISPLAYSURF.blit(sliderVel, (LOCX, LOCY))


    x, y = pygame.mouse.get_pos()

    # If the mouse was pressed on one of the sliders, adjust the color component
    if pygame.mouse.get_pressed()[0]:
        # pg.display.set_caption("PyGame Color Test - " + str(tuple(color)))
        if y > LOCY and y < (LOCY + HEIGHT):
            if x > LOCX and x < (LOCX + WIDTH):
                sliderVelPos = x

    # draw circle for slider to represent current setting
    buttonPos = (sliderVelPos, HEIGHT) 
    pygame.draw.circle(DISPLAYSURF, (255, 255, 255), buttonPos, 20)

    # goal pos
    pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (GOALX, 420), 2)
    pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (GOALX, 440), 2)
    pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (GOALX, 460), 2)

    text_slider = font.render("sliderPos in x = %.1f s" % sliderVelPos, 1, (10, 10, 10))
    text_slider_pos = (0, LOCY + HEIGHT + 10 )
    DISPLAYSURF.blit(text_slider, text_slider_pos)


    # take care of events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE: # space key to launch
                w = (sliderVelPos / WIDTH) * -50
                ballPos = (22,478)
                s = ballPos
                t = 0
                launched = True
                # set the initial velocity
                v0 = (vm*cos(radians(ang)), -vm*sin(radians(ang)))

    keystate = pygame.key.get_pressed()

    if keystate[K_LEFT]: # rotate conterclockwise
        ang+=2
        if ang > 90:
            ang = 90
        cannonMovImg = rot_center(cannonImg, ang)

    if keystate[K_RIGHT]: # rotate clockwise
        ang-=2
        if ang < 0:
            ang = 0
        cannonMovImg = rot_center(cannonImg, ang)

    if keystate[K_UP]: # increase initial speed
        vm+=2

    if keystate[K_DOWN]: # decrease initial speed
        vm-=2

    # display actual scene
    pygame.display.flip()
