import pygame
import random
import sys
from os.path import join
from space_game.player import Player
from space_game.StarBackground import StarBackground
from space_game.laser import Laser
from space_game.Meteor import Meteor
from space_game.meteor_spawing import MeteorSpawner
from space_game.ui import GameUI
from space_game.animatedExplosion import AnimatedExplosion


from pygame.surface import Surface

# Game constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
STAR_COUNT = 64

def setup_display(width: int, height: int) -> Surface:
    pygame.display.set_caption("Space Game")
    display = pygame.display.set_mode((width, height))
    return display

def handle_collisions(player, laser_sprites, meteor_sprites, score, explosion_frames, explosion_sprites):
    """Handle collisions between lasers and meteors, and between player and meteors."""

    # Collision detection between lasers and meteors
    for laser in laser_sprites:
        collided_meteors = pygame.sprite.spritecollide(
            laser,
            meteor_sprites,
            True
        )
        if collided_meteors:
            # Create an animated explosion at the position of the first collided meteor
            AnimatedExplosion(explosion_frames, collided_meteors[0].rect.center, explosion_sprites)
            laser.kill()
            score += len(collided_meteors)
            
    # Collision detection between player and meteors
    if pygame.sprite.spritecollide(
        player,
        meteor_sprites,
        True,
        pygame.sprite.collide_mask
    ):
        player.take_damage(25)

    return score

def main() -> None:
    """Main game loop for the space game."""
    # Initialize pygame
    pygame.init()

    # Set up the display
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT
    screen = setup_display(screen_width, screen_height)

    # Initialize UI manager
    game_ui = GameUI(screen_width, screen_height)

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    laser_sprites = pygame.sprite.Group()
    meteor_sprites = pygame.sprite.Group()
    explosion_sprites = pygame.sprite.Group()

    # Load meteor image once to avoid repeated loading
    meteor_image = pygame.image.load(join("assets", "images", "meteor.png")).convert_alpha()
    # Load explosion frames
    explosion_frames = [
        pygame.image.load(join("assets", "images", "explosion", f"{i}.png")).convert_alpha()
        for i in range(1, 20)
    ]
    # Create the player
    player = Player(screen_width, screen_height)
    all_sprites.add(player)
    # Create the starry background
    stars_background = StarBackground(64, screen_width, screen_height)
    # Create the meteor spawner
    meteor_spawner = MeteorSpawner(screen_width, screen_height, meteor_image, meteor_sprites, all_sprites)

    # Variable to see the score
    score = 0

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                # Pass events to the UI manager
                game_ui.process_event(event)

        # Calculate delta time
        dt = clock.tick(60) / 1000  # Amount of seconds between each loop

        # Game logic updates
        player.update(dt, laser_sprites)
        laser_sprites.update(dt)
        # Update the starry background
        stars_background.update(dt)
        # Meteor spawning
        meteor_spawner.update(dt)
        # Update meteor sprites
        meteor_sprites.update(dt)
        # Update explosion sprites
        explosion_sprites.update(dt)
        # Handle collisions and update score
        score = handle_collisions(player, laser_sprites, meteor_sprites, score, explosion_frames, explosion_sprites)

        # Drawing / rendering
        screen.fill((0, 0, 0))  # Fill the screen with black
        # Draw the starry backgroundaaa
        stars_background.draw(screen)


        # Draw all sprites
        all_sprites.draw(screen)
        # Draw explosion sprites
        explosion_sprites.draw(screen)
        # note where drawing laser and meteor twice may be redundant since they are already part of all_sprites
        # Draw laser sprites
        laser_sprites.draw(screen)
        # Draw meteor sprites
        meteor_sprites.draw(screen)

        # Update UI elements
        game_ui.update(
            dt=dt,
            score=score,
            player_health=player.current_health,
            player_max_health=player.max_health,
            player_can_shoot=player.can_shoot,
            player_laser_shoot_time=player.laser_shoot_time,
            player_cooldown_duration=player.cooldown_duration
        )

        # Draw UI elements on top of everything
        game_ui.draw(screen)

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()