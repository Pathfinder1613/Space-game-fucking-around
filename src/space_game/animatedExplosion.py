import pygame
from os.path import join

class AnimatedExplosion(pygame.sprite.Sprite):
    """class representing an animated explosion in the space game."""

    def __init__(self, frames, pos, group):
        super().__init__(group)
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=pos)
        self.animation_speed = 0.1  # Time in seconds between frames
        self.time_since_last_frame = 0

    def update(self, dt):
        """Update the explosion animation based on delta time."""
        self.time_since_last_frame += dt
        if self.time_since_last_frame >= self.animation_speed:
            self.current_frame += 1
            if self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.kill()  # Remove the sprite when the animation is done
            self.time_since_last_frame = 0

