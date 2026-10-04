import random
import pygame
from os.path import join
from .Meteor import Meteor

class MeteorSpawner:
    """Class to manage the spawning of meteors in the space game."""

    def __init__(self, screen_width, screen_height, meteor_image, meteor_sprites, all_sprites):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.meteor_image = meteor_image
        self.meteor_sprites = meteor_sprites
        self.all_sprites = all_sprites
        self.meteor_spawn_timer = 0
        self.meteor_spawn_delay = 1.0  # Spawn a meteor every 1.0 seconds

    def update(self, dt):
        """Update the meteor spawn timer and spawn meteors if needed."""
        self.meteor_spawn_timer += dt
        if self.meteor_spawn_timer >= self.meteor_spawn_delay:
            self.spawn_meteors(5)  # Spawn 5 meteors at a time
            self.meteor_spawn_timer = 0

    def spawn_meteors(self, amount_of_meteors):
        """Spawn a specified number of meteors at random positions at the top of the screen."""
        for _ in range(amount_of_meteors):
            meteor_x = random.randint(20, self.screen_width - 20)  # Keep away from edges
            meteor_y = 0  # Start at the top of the screen
            meteor = Meteor(self.meteor_image, (meteor_x, meteor_y), self.meteor_sprites, self.screen_width, self.screen_height)
            self.meteor_sprites.add(meteor)
            self.all_sprites.add(meteor)