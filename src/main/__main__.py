""" Imports """
import random
import pygame
import sys
from pygame.locals import *
from pygame.math import Vector2
from pygame.image import load
from vehicle import Vehicle

""" Initialize simulation """
pygame.init()

""" Set frame rate """
fps = 60
framesPerSecond = pygame.time.Clock()

""" Define colors used """
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
D_GREY = (50, 50, 50)
L_GREY = (100, 100, 100)

""" Screen information """
screenWidth = 900
screenHeight = 900

""" Surface information """
displaySurface = pygame.display.set_mode((screenWidth, screenHeight))
displaySurface.fill(BLACK)
pygame.display.set_caption("Task sheet 1 – Getting started")
trajectory = [[-1, -1]] *36000

"""
Create vehicle with the attributes:
- mode:             {"flee", "seek"}
- position:         floats(x, y)
- c_sensor:         float
- c_translation:    float
- c_rotation:       float
"""
random_robot = (random.randrange(screenWidth), random.randrange(screenHeight))
robot = Vehicle("seek", random_robot, 50, 10, 2)
robot_image = pygame.image.load('robot.png')

""" Position the light source """
random_light = (random.randrange(screenWidth), random.randrange(screenHeight))
# light_pos = [400, 400]
light_pos = random_light

""" Simulation Loop """
while True:
    """ Event: quit simulation """
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    """ Update robot simulation """
    robot.move(light_pos)

    if robot.pos[0] > screenWidth:
        robot.pos[0] = 0
    elif robot.pos[0] < 0:
        robot.pos[0] = screenWidth

    if robot.pos[1] > screenHeight:
        robot.pos[1] = 0
    elif robot.pos[1] < 0:
        robot.pos[1] = screenHeight

    """ Update screen """
    displaySurface.fill(BLACK)

    """ draw light and intensity field """
    pygame.draw.circle(displaySurface, WHITE, light_pos, 5)
    for i in range(1, 40):
        pygame.draw.circle(displaySurface, D_GREY, light_pos, 25*i, 1)
    for i in range(1, 10):
        pygame.draw.circle(displaySurface, L_GREY, light_pos, 100*i, 1)

    """ draw trajectory """
    trajectory.append([round(dim) for dim in robot.pos])
    trajectory.pop(0)
    for dot in trajectory: displaySurface.fill(RED, (dot, (1, 1)))

    """ draw robot """
    # pygame.draw.circle(displaySurface, RED, [round(dim) for dim in robot.pos], 2)
    displaySurface.blit(robot_image, [round(dim-15) for dim in robot.pos])

    # Debug
    # pygame.draw.circle(displaySurface, RED, [round(dim) for dim in robot.pos_l], 1)
    # pygame.draw.circle(displaySurface, RED, [round(dim) for dim in robot.pos_r], 1)
    print("Position: ", [round(dim-15) for dim in robot.pos], "Speed: ", round(robot.speed, 2), "FPS: ", str(int(framesPerSecond.get_fps())))

    pygame.display.update()

    """ Wait for next frame """
    framesPerSecond.tick(fps)
