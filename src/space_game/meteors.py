from enum import Enum
import math
import random
import pygame
from os.path import join

from space_game.globals import ALL_SPRITES

from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Group, Sprite


class MeteorType(Enum):
    SMALL  = int(0),
    MEDIUM = int(1),
    LARGE  = int(2)

class Meteor(Sprite):
    ALLOW_SHATTERING: bool = True
    METEOR_IMAGES: list[Surface] = None
    SPRITES = Group()

    def __init__(self: Meteor, type: MeteorType | int, position: Vector2, screen_height: int):
        super().__init__(self.SPRITES, ALL_SPRITES)

        if self.METEOR_IMAGES == None:
            self.METEOR_IMAGES = [
                pygame.image.load(join("assets", "images", "meteor", "small.png")).convert_alpha(),
                pygame.image.load(join("assets", "images", "meteor", "medium.png")).convert_alpha(),
                pygame.image.load(join("assets", "images", "meteor", "large.png")).convert_alpha(),
            ]

        scale = 1 + random.uniform(-0.25, 0.25)

        self.type = type

        self.original_image = pygame.transform.scale_by(self.METEOR_IMAGES[type], scale)
        self.image = self.original_image
        self.rect = self.original_image.get_rect(center = position)

        self.rotation_rate = random.uniform(-20, 20)
        self.rotation = float(0)
        self.speed = 200  # Base speed
        self.screen_height = screen_height

        # Set random angle for movement (0-90 degrees)
        angle_deg = random.uniform(90, 90) + random.uniform(-45, 45)
        angle_rad = math.radians(angle_deg)
        # Calculate velocity components
        self.velocity = pygame.math.Vector2(
            math.cos(angle_rad) * self.speed,
            math.sin(angle_rad) * self.speed
        )
        # Use float-based position for smooth movement
        self.position = pygame.math.Vector2(self.rect.center)
        self.rotation = random.uniform(0, 360)

    def shatter(self: Meteor):
        self.kill()

        if not self.ALLOW_SHATTERING:
            return

        pieces: int = 0
        piece_type: int = self.type - 1

        if (self.type == 0):
            return
        elif (self.type == 1):
            pieces = random.randint(2, 3)
        elif (self.type == 2):
            pieces = random.randint(3, 4)

        for i in range(pieces):
            piece = Meteor(piece_type, self.position, self.screen_height)

            piece.velocity = self.velocity.rotate(random.randint(-20, 20))

    def update(self: Meteor, delta: float):
        self.position += self.velocity * delta
        self.rotation += self.rotation_rate * delta

        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center = self.position)

        if (self.rect.top > self.screen_height):
            self.kill()

class MeteorSpawner:
    def __init__(self: MeteorSpawner, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.spawn_timer = float(0)
        self.spawn_interval = float(1)

    def update(self: MeteorSpawner, delta: float):
        self.spawn_timer += delta

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_meteors(5)  # Spawn 5 meteors at a time
            self.spawn_timer = 0

    def spawn_meteors(self: MeteorSpawner, amount: int):
        for _ in range(amount):
            Meteor(random.randint(0, 2), (random.randint(20, self.screen_width - 20), -64), self.screen_height)