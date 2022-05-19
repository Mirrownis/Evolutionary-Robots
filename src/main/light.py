import pygame, sys, math
from pygame.locals import *


class Light(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("light.png")
        self.rect = self.image.get_rect()
        self.rect.center = (150, 150)

    def draw(self, surface):
        """ draw light """
        surface.blit(self.image, self.rect)