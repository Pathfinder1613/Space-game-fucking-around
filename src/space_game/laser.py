import pygame

from os.path import join

class Laser(pygame.sprite.Sprite):
    """ Class representing a laser shot by the player in the space game."""

    def __init__(self, surf, pos, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = -500  # Negative speed to move upwards
        # self.player_surf = pygame.image.load(join("assets", "images", "player.png")).convert_alpha()

    def update(self, dt):
        """Update the laser's position based on its speed and delta time."""
        self.rect.y += self.speed * dt
        # Remove the laser if it goes off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

    