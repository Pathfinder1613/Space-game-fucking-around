import pygame
from os.path import join
from space_game.laser import Laser

class Player(pygame.sprite.Sprite):
    """Player spaceship controlled by a/d arrow keys."""

    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.player_surf = pygame.image.load(join("assets", "images", "player.png")).convert_alpha()  # Load your spaceship image here
        self.image = pygame.transform.scale(self.player_surf, (64, 64))
        self.rect = self.image.get_rect( center=(screen_width // 2, screen_height - 45))
        self.width = 50
        self.height = 30
        # Position as vector for smooth movement
        self.pos = pygame.math.Vector2((screen_width - self.width) // 2, screen_height - self.height - 45)
        self.rect.center = self.pos
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 300.0
        self.screen_width = screen_width

        # cooldown timer for shooting
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 20

    def handle_event(self, event):
        """Handle keyboard events for movement."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.direction.x -= 1
            elif event.key == pygame.K_d:
                self.direction.x += 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.direction.x += 1
            elif event.key == pygame.K_d:
                self.direction.x -= 1

    def laser_timer(self):
        """Update the shooting cooldown timer."""
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if (current_time - self.laser_shoot_time) / 1000 >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt, laser_sprites):
        """Update player position based on direction and delta time."""
        # Normalize direction to prevent faster diagonal movement (though we only have horizontal)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        # Move the player
        self.pos += self.direction * self.speed * dt
        # Clamp to screen bounds
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > self.screen_width - self.width:
            self.pos.x = self.screen_width - self.width
        # Update rect position
        self.rect.center = self.pos

        recent_keys = pygame.key.get_pressed()
        """ Handle shooting logic based on spacebar press and cooldown."""
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            print("Shoot laser!")  # Placeholder for shooting logic
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()  # Record the time when the laser was shot

        self.laser_timer()  # Update the shooting cooldown timer


    def set_position(self, x, y):
        """Set the player's position."""
        self.rect.center = (x, y)

    def draw(self, screen):
        """Draw the player on the given screen."""
        screen.blit(self.image, self.rect)