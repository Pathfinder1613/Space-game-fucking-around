import pygame
from os.path import join
import random

from pygame.sprite import Sprite
from pygame import Surface

class Star(Sprite):
    def __init__(self):
        self.image = pygame.transform.scale()
        pass

    def update(self, delta: float):
        pass

class StarBackground:
    def __init__(self):
        self.star_size_range = (int(16), int(32))

    def generate_stars(self):
        pass

    def update(self, delta: float):
        pass

    def draw(self, screen: Surface):
        pass