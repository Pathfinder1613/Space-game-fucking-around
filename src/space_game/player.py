import pygame
from os.path import join
from space_game.laser import Laser
from space_game.ship_repository import ShipData


class Player(pygame.sprite.Sprite):
    """Player spaceship controlled by a/d/w/s or arrow keys."""

    def __init__(self, screen_width, screen_height, data: ShipData):
        super().__init__()

        self.player_surf = data.Visual.copy()  # Load your spaceship image here
        self.laser_surf = pygame.image.load(join("assets", "images", "laser.png")).convert_alpha()  # Load laser image
        self.image = pygame.transform.scale(self.player_surf, (64, 64))
        self.rect = self.image.get_rect( center=(screen_width // 2, screen_height - 45))
        self.width = 50
        self.height = 30
        # Position as vector for smooth movement
        self.pos = pygame.math.Vector2((screen_width - self.width) // 2, screen_height - self.height - 45)
        self.rect.center = self.pos
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = data.Speed
        self.screen_width = screen_width
        self.screen_height = screen_height

        # cooldown timer for shooting
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = data.FireRate

        # mask for collision detection
        self.mask = pygame.mask.from_surface(self.image)


        # health tracking
        self.max_health = data.Health
        self.current_health = self.max_health
        self.invulnerable_timer = 0  # For invulnerability after taking damage

    def laser_timer(self):
        """Update the shooting cooldown timer."""
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if (current_time - self.laser_shoot_time) / 1000 >= self.cooldown_duration:
                self.can_shoot = True

    def take_damage(self, amount, sound_manager):
        """Handle player taking damage"""
        if self.invulnerable_timer <= 0:  # Only take damage if not invulnerable
            self.current_health = max(0, self.current_health - amount)
            self.invulnerable_timer = 2.0  # 2 second invulnerability
            if sound_manager:
                sound_manager.play_damage()
            # ship flashes when invulnerable_timer is active, handled in the draw method using pygame mask 

                
                

    def update(self, dt, laser_sprites, sound_manager):
        """Update player position based on currently pressed keys and delta time."""
        # Calculate direction from currently pressed keys
        self.direction = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x -= 1
        if keys[pygame.K_d]:
            self.direction.x += 1
        if keys[pygame.K_w]:
            self.direction.y -= 1
        if keys[pygame.K_s]:
            self.direction.y += 1

        # Normalize direction to prevent faster diagonal movement
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        # Move the player
        self.pos += self.direction * self.speed * dt
        # Clamp to screen bounds
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > self.screen_width - self.width:
            self.pos.x = self.screen_width - self.width

        # Vertical boundary checking
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > self.screen_height - self.height:
            self.pos.y = self.screen_height - self.height

        # Update rect position
        self.rect.center = self.pos

        # Handle shooting
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser = Laser(self.laser_surf, self.rect.midtop)
            if sound_manager:
                sound_manager.play_laser()

        self.laser_timer()  # Update the shooting cooldown timer

        # Update invulnerability timer
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt


    def set_position(self, x, y):
        """Set the player's position."""
        self.rect.center = (x, y)
        self.pos = pygame.math.Vector2((x, y))

    def draw(self, screen):
        """Draw the player on the given screen."""
        screen.blit(self.image, self.rect)

        # Flashing effect while invulnerable
        if self.invulnerable_timer > 0:
            # Flash every 100 milliseconds
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                mask = pygame.mask.from_surface(self.image)
                # Turn the mask into a red surface
                mask_surface = mask.to_surface(
                    setcolor=(255, 0, 0, 100),
                    unsetcolor=(0, 0, 0, 0)
                )
                # Draw the red mask over the player
                screen.blit(mask_surface, self.rect.topleft)
                