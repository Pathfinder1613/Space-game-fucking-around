import pygame
import random
from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.surface import Surface
from pygame.math import Vector2

class Particle(Sprite):
    def __init__(self: Particle, emitter: ParticleEmitter, position: Vector2, size: int, angle: int):
        super().__init__(emitter.particles)

        self.image = Surface((size, size)).convert_alpha()
        self.rect = pygame.draw.circle(
            self.image, 
            (255, 255, 255), 
            (size / 2, size / 2), 
            size / 2
        )

        self.lifetime = 1
        self.time_alive = 0
        self.velocity = Vector2(1, 0).rotate(angle) * float(300)

        self.rect.center = position

    def update(self: Particle, delta_time: float):
        scaling_factor = self.time_alive / self.lifetime

        self.time_alive += delta_time
        self.rect.center += self.velocity * delta_time

        if self.time_alive > self.lifetime:
            self.kill()

class ParticleEmitter:
    def __init__(self: ParticleEmitter):
        self.position = Vector2(0, 0)

        self.emission_rate = float(10)
        self.emission_angle = float(90)
        self.emission_spread = float(5)

        self.emission_interval = 1 / self.emission_rate
        self.emission_timer = 0

        self.particles = Group()

    def update(self: ParticleEmitter, delta_time: float):
        while self.emission_timer > self.emission_interval:
            self.emission_timer -= delta_time
            Particle(self, self.position, 4, self.emission_angle)

        self.emission_timer += delta_time
        self.particles.update(delta_time)

    def draw(self: ParticleEmitter, surface: Surface):
        self.particles.draw(surface)