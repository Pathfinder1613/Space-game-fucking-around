import pygame
import sys
from os.path import join
from space_game.player import Player
from space_game.vfx.stars import StarBackground
from space_game.laser import Laser
from space_game.meteors import Meteor
from space_game.meteors import MeteorSpawner
from space_game.ui.game_ui import GameUI
from space_game.ui.game_over_screen import GameOverScreen
from space_game.ui.pause_menu import PauseMenu
from space_game.ui.main_menu import MainMenu
from space_game.vfx.animated_explosion import AnimatedExplosion
from space_game.sound_manager import SoundManager
from space_game.ship_repository import ShipRepository
from space_game.state import GameState
from space_game.globals import ALL_SPRITES
from space_game.vfx.thrust_particles import ParticleEmitter

from pygame.surface import Surface
from pygame.sprite import Group

# Game constants
# SCREEN_WIDTH = 1280
# SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
STAR_COUNT = 128
unused_troll_variable = "(:"

def setup_display(width: int, height: int) -> Surface:
    pygame.display.set_caption("Space Game")
    display = pygame.display.set_mode((width, height))
    return display

def handle_collisions(player, laser_sprites, meteor_sprites, score, explosion_frames, explosion_sprites, sound_manager):
    """Handle collisions between lasers and meteors, and between player and meteors."""

    # Collision detection between lasers and meteors
    for laser in laser_sprites:
        collided_meteors: list[Meteor] = pygame.sprite.spritecollide(
            laser,
            meteor_sprites,
            False
        )

        if collided_meteors:
            sound_manager.play_explosion()
            laser.kill()

            for i in range(len(collided_meteors)):
                AnimatedExplosion(explosion_frames, collided_meteors[i].rect.center, explosion_sprites)
                collided_meteors[i].shatter()
                score += len(collided_meteors)

    # Collision detection between player and meteors
    if pygame.sprite.spritecollide(
        player,
        meteor_sprites,
        True,
        pygame.sprite.collide_mask
    ):
        player.take_damage(25, sound_manager)

    return score

def update_ui(game_ui, dt, score, player):
    """Update the UI elements with the current game state."""
    game_ui.update(
        dt=dt,
        score=score,
        player_health=player.current_health,
        player_max_health=player.max_health,
        player_can_shoot=player.can_shoot,
        player_laser_shoot_time=player.laser_shoot_time,
        player_cooldown_duration=player.cooldown_duration
    )

def main() -> None:
    """Main game loop for the space game."""
    # Initialize pygame
    pygame.init()

    # Set up the display
    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT
    screen = setup_display(screen_width, screen_height)

    ship_repository = ShipRepository()

    # Initialize UI manager
    game_ui = GameUI(screen_width, screen_height)
    pause_menu = PauseMenu(screen_width, screen_height)
    main_menu = MainMenu(screen, ship_repository)

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    menu_running = True
    while menu_running:
        delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            main_menu.handle_event(event)

        main_menu.update(delta)

        screen.fill((0, 0, 0))

        main_menu.draw()

        pygame.display.flip()

        # Check what the menu wants to do
        if main_menu.state == GameState.GAMEPLAY:
            menu_running = False

        elif main_menu.state == GameState.EXITING:
            pygame.quit()
            sys.exit()

    # Create sprite groups
    laser_sprites = Laser.SPRITES  # Use the class-level laser group
    meteor_sprites = Meteor.SPRITES  # Use the class-level meteor group
    explosion_sprites = pygame.sprite.Group()
    
    # Load explosion frames
    explosion_frames = [
        pygame.transform.scale_by(pygame.image.load(join("assets", "images", "explosion", f"{i}.png")).convert_alpha(), 3)
        for i in range(1, 20)
    ]
    # Create the player
    player = Player(screen_width, screen_height, main_menu.ships[main_menu.selected_ship])
    ALL_SPRITES.add(player)
    # Create the starry background
    stars_background = StarBackground(STAR_COUNT, screen_width, screen_height, 4)
    # Create the meteor spawner

    test_emitter = ParticleEmitter()
    test_emitter.position = player.pos

    meteor_spawner = MeteorSpawner(screen_width, screen_height)

    # Initialize sound manager
    sound_manager = SoundManager()
    sound_manager.play_background_music()  # Start background music
    # Initialize pause menu
    pause_menu = PauseMenu(screen_width, screen_height)

    # Variable to see the score
    score = 0

    # Main game loop
    running = True
    paused = False
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

            game_ui.process_event(event)

        # Calculate delta time
        delta = clock.tick(60) / 1000  # Amount of seconds between each loop

        # Game logic updates
        if not paused:
            player.update(delta, laser_sprites, sound_manager)  # Pass sound manager to player
            laser_sprites.update(delta)
            # Update the starry background
            stars_background.update(delta)

            test_emitter.update(delta)
            # Meteor spawning
            meteor_spawner.update(delta)
            # Update meteor sprites
            meteor_sprites.update(delta)
            # Update explosion sprites
            explosion_sprites.update(delta * 8)
            # Handle collisions and update score
            score = handle_collisions(player, laser_sprites, meteor_sprites, score, explosion_frames, explosion_sprites, sound_manager)

        # Drawing / rendering
        screen.fill((0, 0, 0))  # Fill the screen with black
        # Draw the starry background
        stars_background.draw(screen)
        test_emitter.draw(screen)

        # Draw all sprites (includes player, lasers, and meteors)
        ALL_SPRITES.draw(screen)
        # Draw explosion sprites
        explosion_sprites.draw(screen)

        # Update UI elements
        update_ui(game_ui, delta, score, player)

        # Draw UI elements on top of everything
        game_ui.draw(screen)
        
        # Draw pause menu if paused
        if paused:
            pause_menu.update(delta)
            pause_menu.draw(screen)

        # Update the display
        pygame.display.flip()

        # Check for ESC key press to exit the game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        # Check if player is dead and show game over screen
        if player.current_health <= 0:
            # Show game over screen using pygame_gui
            update_ui(game_ui, delta, score, player)
            game_ui.draw(screen)
            pygame.display.flip()

            game_over_screen = GameOverScreen(screen_width, screen_height)
            game_over_screen.score_label.set_text(f'Final Score: {score}')
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                # Update the game over screen UI
                game_over_screen.ui_manager.update(delta)
                # turn off the background music
                sound_manager.stop_background_music()
                # Draw the game over screen
                game_over_screen.ui_manager.draw_ui(screen)
                pygame.display.flip()

    # Quit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()