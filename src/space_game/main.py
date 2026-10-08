import pygame
import sys
import pygame_gui
from os.path import join
from space_game.entities.player import Player
from space_game.entities.stars import StarBackground
from space_game.entities.projectiles.laser import Laser
from space_game.entities.enemies.meteors import Meteor
from space_game.entities.enemies.meteors import MeteorSpawner
from space_game.Ui.game_ui import GameUI
from space_game.Ui.game_over_screen import GameOverScreen
from space_game.Ui.pause_menu import PauseMenu
from space_game.Ui.main_menu import MainMenu
from space_game.entities.effects.animated_explosion import AnimatedExplosion
from space_game.core.globals import ALL_SPRITES
from space_game.audio.sound_manager import SoundManager
from space_game.core.ship_repository import ShipRepository
from space_game.core.state import GameState

from pygame.surface import Surface
from pygame.sprite import Group


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
STAR_COUNT = 128

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
    pygame.init()

    screen_width = SCREEN_WIDTH
    screen_height = SCREEN_HEIGHT

    screen = setup_display(screen_width, screen_height)

    clock = pygame.time.Clock()

    # Game state
    game_state = GameState.MAIN_MENU

    # Repositories / UI
    ship_repository = ShipRepository()
    game_ui = GameUI(
        screen_width,
        screen_height
    )
    pause_menu = PauseMenu(
        screen_width,
        screen_height
    )
    main_menu = MainMenu(
        screen,
        ship_repository
    )

    # Game objects
    laser_sprites = Laser.SPRITES
    meteor_sprites = Meteor.SPRITES
    explosion_sprites = pygame.sprite.Group()

    explosion_frames = [
        pygame.transform.scale_by(
            pygame.image.load(
                join(
                    "assets",
                    "images",
                    "explosion",
                    f"{i}.png"
                )
            ).convert_alpha(),
            3
        )
        for i in range(1, 20)
    ]

    player = None
    stars_background = None
    meteor_spawner = None
    sound_manager = None

    score = 0

    # Main loop
    while game_state != GameState.EXITING:
        dt = clock.tick(60) / 1000.0
        # Events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = GameState.EXITING
                continue

            # # MAIN MENU
            if game_state == GameState.MAIN_MENU:
                main_menu.handle_event(event)
                if main_menu.state == GameState.GAMEPLAY:
                    player = Player(
                        screen_width,
                        screen_height,
                        main_menu.ships[
                            main_menu.selected_ship
                        ]
                    )

                    ALL_SPRITES.add(player)

                    stars_background = StarBackground(
                        STAR_COUNT,
                        screen_width,
                        screen_height,
                        4
                    )

                    meteor_spawner = MeteorSpawner(
                        screen_width,
                        screen_height
                    )

                    sound_manager = SoundManager()
                    sound_manager.play_background_music()

                    score = 0

                    game_state = GameState.GAMEPLAY

                elif main_menu.state == GameState.EXITING:
                    game_state = GameState.EXITING

            # GAMEPLAY
            elif game_state == GameState.GAMEPLAY:
                game_ui.process_event(event)

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_p:
                        game_state = GameState.PAUSED

                    elif event.key == pygame.K_ESCAPE:
                        game_state = GameState.PAUSED

            # PAUSED
            elif game_state == GameState.PAUSED:

                new_state = pause_menu.handle_event(event)

                if new_state is not None:
                    game_state = new_state

                # Allow P / ESC to resume
                if event.type == pygame.KEYDOWN:
                    if event.key in (
                        pygame.K_p,
                        pygame.K_ESCAPE
                    ):
                        game_state = GameState.GAMEPLAY

            # GAME OVER

            elif game_state == GameState.GAME_OVER:

                new_state = GameOverScreen.handle_event(event)

                if new_state is not None:
                    game_state = new_state 

        # UPDATE
        if game_state == GameState.MAIN_MENU:

            main_menu.update(dt)

        elif game_state == GameState.GAMEPLAY:

            player.update(
                dt,
                laser_sprites,
                sound_manager
            )

            laser_sprites.update(dt)
            stars_background.update(dt)
            meteor_spawner.update(dt)
            meteor_sprites.update(dt)
            explosion_sprites.update(dt * 8)

            score = handle_collisions(
                player,
                laser_sprites,
                meteor_sprites,
                score,
                explosion_frames,
                explosion_sprites,
                sound_manager
            )

            update_ui(
                game_ui,
                dt,
                score,
                player
            )

            # Check player death
            if player.current_health <= 0:

                sound_manager.stop_background_music()

                game_over_screen = GameOverScreen(
                    screen_width,
                    screen_height
                )

                game_over_screen.score_label.set_text(
                    f"Final Score: {score}"
                )

                game_state = GameState.GAME_OVER

        elif game_state == GameState.PAUSED:

            pause_menu.update(dt)

        elif game_state == GameState.GAME_OVER:

            game_over_screen.ui_manager.update(dt)

        # DRAW
        screen.fill((0, 0, 0))

        if game_state == GameState.MAIN_MENU:

            main_menu.draw()

        elif game_state == GameState.GAMEPLAY:

            stars_background.draw(screen)

            ALL_SPRITES.draw(screen)

            explosion_sprites.draw(screen)

            game_ui.draw(screen)

        elif game_state == GameState.PAUSED:

            # Draw the game underneath the pause menu

            stars_background.draw(screen)

            ALL_SPRITES.draw(screen)

            explosion_sprites.draw(screen)

            game_ui.draw(screen)

            pause_menu.draw(screen)

        elif game_state == GameState.GAME_OVER:
            stars_background.draw(screen)
            ALL_SPRITES.draw(screen)
            explosion_sprites.draw(screen)
            game_ui.draw(screen)
            game_over_screen.draw(screen)

        pygame.display.flip()

    # Shutdown
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
