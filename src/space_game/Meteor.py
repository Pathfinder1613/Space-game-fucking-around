import pygame
import math
import random
from os.path import join
from pygame.sprite import Sprite
from pygame.math import Vector2

class Meteor(Sprite):
    """Class representing a meteor in the space game."""

    def __init__(self, surf, pos, group, screen_width, screen_height):
        super().__init__(group)

        self.original_image = surf

        # Set random scale for the meteor
        scale_factor = random.uniform(0.5, 1.5)
        scaled_width = int(self.original_image.get_width() * scale_factor)
        scaled_height = int(self.original_image.get_height() * scale_factor)
        self.image = pygame.transform.scale(
            self.original_image,
            (scaled_width, scaled_height)
        )
        self.original_image = self.image  # For rotation purposes

        self.rect = self.image.get_rect(midtop=pos)

        # Store screen dimensions for bounds checking
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Random angle between -30 and 30 degrees (mostly downward with slight variation)
        angle_deg = random.uniform(-30, 30)
        angle_rad = math.radians(angle_deg)

        # Base speed in pixels per second
        self.speed = 200
        self.velocity = Vector2(
            math.sin(angle_rad) * self.speed,
            math.cos(angle_rad) * self.speed
        )

        # Use float-based position for smooth movement
        self.position = Vector2(self.rect.center)

        # Rotation properties
        self.rotation_rate = random.uniform(-20, 20)  # Degrees per second
        self.rotation = random.uniform(0, 360)  # Initial random rotation

    def update(self, dt):
        """Update the meteor's position based on its velocity and delta time."""
        # Move based on velocity
        self.position += self.velocity * dt
        self.rect.center = self.position

        # Rotate the meteor
        self.rotation += self.rotation_rate * dt

        # Rotate the image and keep it centered
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Check if meteor is off the screen and remove it
        if (
            self.rect.top > self.screen_height
            or self.rect.bottom < 0
            or self.rect.left > self.screen_width
            or self.rect.right < 0
        ):
            self.kill()