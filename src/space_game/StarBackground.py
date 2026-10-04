import pygame
from os.path import join
import random

from pygame.sprite import Sprite
from pygame import Surface
from pygame.sprite import Group
from pygame.math import Vector2

class Star(Sprite):
    SPRITES = Group()

    def __init__(self: Star, image: Surface, position: Vector2):
        super().__init__(self.SPRITES)

        size = random.randint(8, 16)

        self.image = pygame.transform.scale(image, (size, size))

        self.rect = image.get_rect(center = position)
        self.position = Vector2(self.rect.center)
        self.speed = float(16) + (size - 8) * 8

    def update(self: Star, delta: float):
        self.position.y += self.speed * delta
        self.rect.center = self.position

        if self.rect.top > 720:
            self.position = Vector2(random.randint(0, 1280), -16)

class StarBackground:
    def __init__(self: StarBackground, stars: int, speed_multiplier: float = 1):
        self.star_image = pygame.image.load(join("assets", "images", "star.png")).convert_alpha()
        self.star_image = pygame.transform.scale(self.star_image, (16, 16))
        
        self.star_sprites = Group()
        self.speed_multiplier = speed_multiplier
        
        self.generate_stars(stars)

    def generate_stars(self: StarBackground, amount: int):
        for i in range(amount):
            self.star_sprites.add(Star(self.star_image, (random.randint(0, 1280), random.randint(0, 720))))

    def update(self: StarBackground, delta: float):
        self.star_sprites.update(delta * self.speed_multiplier)
        pass

    def draw(self: StarBackground, screen: Surface):
        self.star_sprites.draw(screen)
        pass