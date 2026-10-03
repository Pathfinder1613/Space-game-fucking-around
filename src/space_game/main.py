import pygame
import random
import sys
from os.path import join
from space_game.player import Player
from space_game.starsBackground import StarsBackground
from space_game.laser import Laser
from space_game.Meteor import Meteor
from space_game.meteor_spawing import MeteorSpawner

def main() -> None:
    """Main game loop for the space game."""
    # Initialize pygame
    pygame.init()

    # Set up the display
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Game")

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    laser_sprites = pygame.sprite.Group()
    meteor_sprites = pygame.sprite.Group()

    # Load meteor image once to avoid repeated loading
    meteor_image = pygame.image.load(join("assets", "images", "meteor.png")).convert_alpha()

    # Create the player
    player = Player(screen_width, screen_height)
    all_sprites.add(player)

    # Create the starry background
    stars_background = StarsBackground(screen_width, screen_height)

    # Create the meteor spawner
    meteor_spawner = MeteorSpawner(screen_width, screen_height, meteor_image, meteor_sprites, all_sprites)

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                # Pass events to the player for handling
                player.handle_event(event)

        # Calculate delta time
        dt = clock.tick(60) / 1000  # Amount of seconds between each loop

        # Game logic updates
        player.update(dt, laser_sprites)
        laser_sprites.update(dt)

        # Update the meteor spawner
        meteor_spawner.update(dt)

        # Drawing / rendering
        screen.fill((0, 0, 0))  # Fill the screen with black
        # Draw the starry background
        stars_background.draw(screen)
        # Draw all sprites
        all_sprites.draw(screen)
        # Draw laser sprites
        laser_sprites.draw(screen)
        # Draw meteor sprites
        meteor_sprites.draw(screen)

        # collision detection between lasers and meteors
        for laser in laser_sprites:
            collided_meteors = pygame.sprite.spritecollide(laser, meteor_sprites, True)  # Remove meteors on collision
            if collided_meteors:
                laser.kill()  # Remove the laser if it hits a meteor

        meteor_sprites.update(dt)  # Update meteor positions

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()