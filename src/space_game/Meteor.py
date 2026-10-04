import pygame
import math
import random
from os.path import join

class Meteor(pygame.sprite.Sprite):
    """Class representing a meteor in the space game."""

    def __init__(self, surf, pos, group, screen_width, screen_height):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = 200  # Base speed
        # self.spawn_amount = 5  # Number of meteors to spawn
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Set random angle for movement (0-90 degrees)
        angle_deg = random.uniform(0, 260)
        angle_rad = math.radians(angle_deg)
        # Calculate velocity components
        self.velocity = pygame.math.Vector2(
            math.cos(angle_rad) * self.speed,
            math.sin(angle_rad) * self.speed
        )
        # Use float-based position for smooth movement
        self.position = pygame.math.Vector2(self.rect.center)

    def update(self, dt):
        """Update the meteor's position based on its velocity and delta time."""
        # Move based on velocity
        self.position += self.velocity * dt
        self.rect.center = self.position

        # check if meteor is off the screen and remove it
        if (self.rect.top > self.screen_height):
            self.kill()

            

    # # Meteor spawning
    #         meteor_spawn_timer += dt
    #         if meteor_spawn_timer >= meteor_spawn_delay:
    #             for _ in range(amount_of_meteors):
    #                 # Spawn a meteor at a random position at the top of the screen
    #                 meteor_x = random.randint(20, screen_width - 20)  # Keep away from edges
    #                 meteor_y = -50  # Start slightly above the screen
    #                 meteor = Meteor(meteor_image, (meteor_x, meteor_y), meteor_sprites, screen_width, screen_height)
    #                 meteor_sprites.add(meteor)
    #                 all_sprites.add(meteor)
    #                 meteor_spawn_timer = 0
    
    #         # Update meteor sprites
    #         meteor_sprites.update(dt)

    

    