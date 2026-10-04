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

        # Set random angle for movement (0 to 100 degrees - downward only in pygame coordinates)
        angle_deg = random.uniform(0, -100)
        angle_rad = math.radians(angle_deg)
        # Calculate velocity components (note: negate y for pygame coordinates where y increases downward)
        self.velocity = pygame.math.Vector2(
            math.cos(angle_rad) * self.speed,
            -math.sin(angle_rad) * self.speed
        )
        # Use float-based position for smooth movement
        self.position = pygame.math.Vector2(self.rect.center)

        # Set random scale for the meteor
        scale_factor = random.uniform(0.5, 1.5)
        # Store center before scaling
        old_center = self.rect.center
        # Scale the image
        new_width = int(self.rect.width * scale_factor)
        new_height = int(self.rect.height * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        # Update rect to match new image size, preserving center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        # Set initial random rotation
        self.rotation = random.uniform(0, 360)

    def update(self, dt):
        """Update the meteor's position based on its velocity and delta time."""
        # Move based on velocity
        self.position += self.velocity * dt
        self.rect.center = self.position

        self.rotation += self.rotation_rate * dt

        # rotate the meteor slowly using original image to avoid quality loss
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

        # check if meteor is off the screen and remove it
        if (self.rect.top > self.screen_height or
            self.rect.bottom < 0 or
            self.rect.left > self.screen_width or
            self.rect.right < 0):
            self.kill()


    

    