import pygame
import math
import random
from os.path import join

from pygame.surface import Surface
from pygame.sprite import Sprite

class Meteor(Sprite):
    """Class representing a meteor in the space game."""

    def __init__(self, surf: Surface, pos, group, screen_width, screen_height):
        super().__init__(group)

        scale = 1 + (random.randint(-1000, 1000) / 1000) * 0.25
        self.original_image = pygame.transform.scale(surf, (surf.width * scale, surf.height * scale))

        self.image = surf
        self.rect = self.image.get_rect(center=pos)

        self.rotation_rate = random.normalvariate(0, 20)
        self.rotation = float(0)
        self.speed = 200  # Base speed

        # self.spawn_amount = 5  # Number of meteors to spawn
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Set random angle for movement (0-90 degrees)
        angle_deg = random.uniform(90, 90) + random.normalvariate(0, 45)
        angle_rad = math.radians(angle_deg)
        # Calculate velocity components
        self.velocity = pygame.math.Vector2(
            math.cos(angle_rad) * self.speed,
            math.sin(angle_rad) * self.speed
        )
        # Use float-based position for smooth movement
        self.position = pygame.math.Vector2(self.rect.center)
        
        self.rotation = random.uniform(0, 360)
        self.image = pygame.transform.rotate(self.original_image, self.rotation)

    def update(self, dt):
        """Update the meteor's position based on its velocity and delta time."""
        # Move based on velocity
        self.position += self.velocity * dt
        self.rect.center = self.position

        self.rotation += self.rotation_rate * dt

        # rotate the meteor slowly
        self.image = pygame.transform.rotate(self.original_image, self.rotation)

        # check if meteor is off the screen and remove it
        if (self.rect.top > self.screen_height):
            self.kill()


    

    