import pygame
from os.path import join

from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.math import Vector2

from space_game.core.globals import ALL_SPRITES

class Laser(Sprite):
    """Class representing a laser beam fired by the player."""
    SPRITES = Group()

    def __init__(self, image: Surface, position: Vector2):
        super().__init__(self.SPRITES, ALL_SPRITES)
        self.image = image.copy()
        self.image.fill((255, 0, 0, 255), special_flags = pygame.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect(midbottom = position)
        self.speed = float(-500)  # Negative speed to move upwards

    def update(self, delta: float):
        """Update the laser's position."""
        self.rect.y += self.speed * delta
        # Remove the laser if it goes off the top of the screen
        if self.rect.bottom < 0:
            self.kill()