import pygame
from os.path import join
import random

class StarsBackground(pygame.sprite.Sprite):
    """Class to manage the starry background for the space game."""

    def __init__(self, screen_width, screen_height, num_stars=20):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_stars = num_stars
        self.stars = self.generate_stars()
        self.star_img = pygame.image.load(join("assets", "images", "star.png")).convert_alpha()  # Load your star image here
        self.star_img = pygame.transform.scale(self.star_img, (10, 10))  # Scale star image to a smaller size
        

    def generate_stars(self):
        """Generate a list of star positions."""
        stars = []
        for _ in range(self.num_stars):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            stars.append((x, y))
        return stars

    def update(self, dt):
        """Update the star positions to create a scrolling effect."""
        # Move stars downwards
        new_stars = []
        for x, y in self.stars:
            y += 50 * dt  # Move down at a speed of 50 pixels per second
            if y > self.screen_height:
                y = 0  # Reset to top if it goes off the bottom
                x = random.randint(0, self.screen_width)  # Randomize x position when resetting
            new_stars.append((x, y))
        self.stars = new_stars

    def draw(self, screen):
        """Draw the stars on the given screen."""
        for star in self.stars:
            screen.blit(self.star_img, star)  # Draw each star as an image