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

    def spawn_meteors(self, amount_of_meteors):
        """Spawn a specified number of meteors at random positions at the top of the screen."""
        for _ in range(amount_of_meteors):
            meteor_x = random.randint(20, self.screen_width - 20)  # Keep away from edges
            meteor_y = 0  # Start at the top of the screen
            meteor = Meteor(self.meteor_image, (meteor_x, meteor_y), self.meteor_sprites, self.screen_width, self.screen_height)
            self.meteor_sprites.add(meteor)
            self.all_sprites.add(meteor)