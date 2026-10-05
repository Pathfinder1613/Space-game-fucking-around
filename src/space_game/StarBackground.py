import pygame
import random
from os.path import join
from pygame.sprite import Sprite
from pygame import Surface
from pygame.sprite import Group
from pygame.math import Vector2

class Star(Sprite):
    """Class representing a single star in the background."""

    def __init__(self, image: Surface, position: Vector2, screen_width: int, screen_height: int):
        super().__init__()

        size = random.randint(8, 16)
        self.image = pygame.transform.scale(image, (size, size))

        self.rect = self.image.get_rect(center=position)
        self.position = Vector2(self.rect.center)
        self.speed = float(20) + (size - 8) * 2  # Speed range: 20-36 based on size
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, delta: float):
        """Update the star's position."""
        self.position.y += self.speed * delta
        self.rect.center = self.position

        # Wrap around to top if moved off bottom of screen
        if self.rect.top > self.screen_height:
            self.position = Vector2(
                random.randint(0, self.screen_width),
                -16
            )

class StarBackground:
    """Class managing the starry background."""

    def __init__(self, stars: int, screen_width: int, screen_height: int, speed_multiplier: float = 1):
        self.star_sprite = pygame.image.load(join("assets", "images", "star.png")).convert_alpha()
        self.star_sprites = Group()
        self.speed_multiplier = speed_multiplier
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.generate_stars(stars)

    def generate_stars(self, amount: int):
        """Generate and add stars to the background."""
        for i in range(amount):
            position = Vector2(
                random.randint(0, self.screen_width),
                random.randint(0, self.screen_height)
            )
            self.star_sprites.add(Star(self.star_sprite, position, self.screen_width, self.screen_height))

    def update(self, delta: float):
        """Update all stars in the background."""
        self.star_sprites.update(delta * self.speed_multiplier)

    def draw(self, screen: Surface):
        """Draw all stars to the screen."""
        self.star_sprites.draw(screen)