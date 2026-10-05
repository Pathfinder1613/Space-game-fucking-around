import random
import pygame
from os.path import join

from .Meteor import Meteor

from pygame.sprite import Group

class MeteorSpawner:
    def __init__(self: MeteorSpawner, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.meteor_image = pygame.image.load(join("assets", "images", "meteor.png")).convert_alpha()

        self.spawn_timer = float(0)
        self.spawn_interval = float(1)

    def update(self: MeteorSpawner, delta: float):
        self.spawn_timer += delta

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_meteors(5)  # Spawn 5 meteors at a time
            self.spawn_timer = 0

    def spawn_meteors(self: MeteorSpawner, amount: int):
        for _ in range(amount):
            Meteor(self.meteor_image, (random.randint(20, self.screen_width - 20), -64), self.screen_height)