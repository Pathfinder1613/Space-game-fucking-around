import pygame
import random
import sys
from os.path import join
from space_game.player import Player
from space_game.starsBackground import StarsBackground
from space_game.laser import Laser
from space_game.Meteor import Meteor

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

    # Meteor spawning
    meteor_spawn_timer = 0
    meteor_spawn_delay = 1.5  # Spawn a meteor every 1.5 seconds

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

        # Meteor spawning
        meteor_spawn_timer += dt
        if meteor_spawn_timer >= meteor_spawn_delay:
            # Spawn a meteor at a random position at the top of the screen
            meteor_x = random.randint(20, screen_width - 20)  # Keep away from edges
            meteor_y = -50  # Start slightly above the screen
            meteor = Meteor(meteor_image, (meteor_x, meteor_y), meteor_sprites, screen_width, screen_height)
            meteor_sprites.add(meteor)
            all_sprites.add(meteor)
            meteor_spawn_timer = 0

        # Update meteor sprites
        meteor_sprites.update(dt)

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

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()