import pygame
from os.path import join
import random

from pygame.sprite import Sprite
from pygame import Surface
from pygame.sprite import Group
from pygame.math import Vector2

class Star(Sprite):
    def __init__(self: Star, image: Surface, position: Vector2, screen_width: int, screen_height: int):
        super().__init__()

        size = random.randint(8, 16)

        self.image = pygame.transform.scale(image, (size, size))
        self.rect = image.get_rect(center = position)
        self.position = Vector2(self.rect.center)
        self.speed = float(20) + (size - 8) * 2  # Reduced range: 20-36 instead of 16-80
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self: Star, delta: float):
        self.position.y += self.speed * delta
        self.rect.center = self.position

        if self.rect.top > self.screen_height:
            self.position = Vector2(random.randint(0, self.screen_width), -16)

class StarBackground:
    def __init__(self: StarBackground, stars: int, screen_width: int, screen_height: int, speed_multiplier: float = 1):
        self.star_sprite = pygame.image.load(join("assets", "images", "star.png")).convert_alpha()
        self.star_sprites = Group()
        self.speed_multiplier = speed_multiplier
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.generate_stars(stars)

    def generate_stars(self: StarBackground, amount: int):
        for i in range(amount):
            self.star_sprites.add(Star(self.star_sprite,
                                     (random.randint(0, self.screen_width),
                                      random.randint(0, self.screen_height)),
                                     self.screen_width,
                                     self.screen_height))

    def update(self: StarBackground, delta: float):
        self.star_sprites.update(delta * self.speed_multiplier)
        pass

    def draw(self: StarBackground, screen: Surface):
        self.star_sprites.draw(screen)
        pass