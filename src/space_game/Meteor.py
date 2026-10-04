import pygame
import math
import random
from os.path import join

from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame.math import Vector2

class Meteor(Sprite):
    """Class representing a meteor in the space game."""

    def __init__(self: Meteor, image: Surface, position: Vector2):
        super().__init__()

        scale = 1 + random.uniform(-0.25, 0.25)
        self.original_image = pygame.transform.scale_by(image, scale)
        self.image = self.original_image
        self.rect = self.original_image.get_rect(center = position)

        self.rotation_rate = random.uniform(-20, 20)
        self.rotation = float(0)
        self.speed = 200  # Base speed

        # Set random angle for movement (0-90 degrees)
        angle_deg = random.uniform(90, 90) + random.uniform(-45, 45)
        angle_rad = math.radians(angle_deg)
        # Calculate velocity components
        self.velocity = pygame.math.Vector2(
            math.cos(angle_rad) * self.speed,
            math.sin(angle_rad) * self.speed
        )
        # Use float-based position for smooth movement
        self.position = pygame.math.Vector2(self.rect.center)
        self.rotation = random.uniform(0, 360)

    def update(self: Meteor, delta: float, screen: Surface):
        self.position += self.velocity * delta
        self.rotation += self.rotation_rate * delta

        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center = self.position)

        if (self.rect.top > screen.height):
            self.kill()