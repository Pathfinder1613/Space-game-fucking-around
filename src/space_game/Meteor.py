import pygame
import math
import random
from os.path import join


class Meteor(pygame.sprite.Sprite):
    """Class representing a meteor in the space game."""

    def __init__(self, surf, pos, group, screen_width, screen_height):
        super().__init__(group)

        self.original_image = surf

        self.image = surf
        self.rect = self.image.get_rect(midtop=pos)

        self.rotation_rate = random.normalvariate(0, 20)
        self.rotation = float(0)
        self.speed = 200  # Base speed in pixels per second

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Random angle between -30 and 30 degrees
        angle_deg = random.uniform(-30, 30)
        angle_rad = math.radians(angle_deg)

        self.velocity = pygame.math.Vector2(
            math.sin(angle_rad) * self.speed,
            math.cos(angle_rad) * self.speed
        )

        # Use float-based position for smooth movement
        self.position = pygame.math.Vector2(self.rect.center)

        # Set random scale for the meteor
        scale_factor = random.uniform(0.5, 1.5)

        # Calculate scaled size
        new_width = int(self.rect.width * scale_factor)
        new_height = int(self.rect.height * scale_factor)

        # Scale the original image
        self.image = pygame.transform.scale(
            self.original_image,
            (new_width, new_height)
        )

        # Make the scaled image the source for rotation
        self.original_image = self.image

        # Update rect to match scaled image
        self.rect = self.image.get_rect(center=self.rect.center)

        # Set initial random rotation
        self.rotation = random.uniform(0, 360)

    def update(self, dt):
        """Update the meteor's position based on its velocity and delta time."""

        # Move based on velocity
        self.position += self.velocity * dt
        self.rect.center = self.position

        # Rotate the meteor
        self.rotation += self.rotation_rate * dt

        # Rotate the scaled image
        self.image = pygame.transform.rotate(
            self.original_image,
            self.rotation
        )

        # Keep the meteor centered while rotating
        self.rect = self.image.get_rect(center=self.rect.center)

        # Check if meteor is off the screen and remove it
        if (
            self.rect.top > self.screen_height
            or self.rect.bottom < 0
            or self.rect.left > self.screen_width
            or self.rect.right < 0
        ):
            self.kill()

