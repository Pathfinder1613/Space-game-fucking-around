import random
import pygame
from os.path import join

from .Meteor import Meteor

from pygame.surface import Surface
from pygame.sprite import Group
from enum import Enum

class MeteorSize(Enum):
    SMALL = 0,
    MEDIUM = 1,
    LARGE = 2,

class MeteorType(Enum):
    NORMAL = 0

class MeteorSpawner:
    def __init__(self: MeteorSpawner, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.small_meteor_image = pygame.image.load(join("assets", "images", "meteor", "small.png")).convert_alpha()
        self.medium_meteor_image = pygame.image.load(join("assets", "images", "meteor", "medium.png")).convert_alpha()
        self.large_meteor_image = pygame.image.load(join("assets", "images", "meteor", "large.png")).convert_alpha()

        self.spawn_timer = float(0)
        self.spawn_interval = float(1)

    def update(self: MeteorSpawner, delta: float):
        self.spawn_timer += delta

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_meteors(5)  # Spawn 5 meteors at a time
            self.spawn_timer = 0

    def spawn_meteors(self: MeteorSpawner, amount: int):
        for _ in range(amount):
            images = [
                self.small_meteor_image, 
                self.medium_meteor_image, 
                self.large_meteor_image,
            ]

            Meteor(images[random.randint(0, len(images) - 1)], (random.randint(20, self.screen_width - 20), -64), self.screen_height)