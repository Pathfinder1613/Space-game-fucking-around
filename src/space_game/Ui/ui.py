import pygame
import pygame_gui
from os.path import join
from pathlib import Path

class ProgressBarWithNoText(pygame_gui.elements.UIProgressBar):
    def status_text(self):
        return ""

class GameUI:
    """Manages all pygame-gui elements for the space game."""

    def __init__(self, screen_width, screen_height):
        """Initialize the UI manager and create UI elements."""
        self.ui_manager = pygame_gui.UIManager((screen_width, screen_height))

        self.ui_manager.add_font_paths(
            font_name = "oxanium",
            regular_path = "assets/fonts/Oxanium-Bold.ttf",
            bold_path = "assets/fonts/Oxanium-Bold.tff"
        )

        # Load UI theme for better visuals
        try:
            self.ui_manager.get_theme().load_theme(join("assets", "ui_theme.json"))
        except FileNotFoundError:
            print("Warning: ui_theme.json not found, using default theme")
        except Exception as e:
            print(f"Error loading ui_theme.json: {e}")

        # Score label (can remain as text)
        self.score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (200, 30)),
            text='Score: 0',
            manager=self.ui_manager,
            object_id='#score_label'
        )

        # Health progress bar with label
        self.health_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 50), (80, 25)),
            text='Health:',
            manager=self.ui_manager,
            object_id='#health_label_text'
        )

        self.health_bar = pygame_gui.elements.UIProgressBar(
            relative_rect=pygame.Rect((90, 50), (200, 25)),
            manager=self.ui_manager,
            object_id='#health_bar'
        )

        left = 10
        right = 5
        self.cooldown_bar = ProgressBarWithNoText(
            relative_rect = pygame.Rect(left * 2 - 128, -64, 128 - left * 2 - right * 2, 64),
            manager       = self.ui_manager,
            anchors       = {"bottom": "bottom", "right": "right"},
            object_id     = '#cooldown_bar'
        )

        weapon_display_image = pygame.image.load(join("assets", "ui", "WeaponIcon_PulseLaser.png")).convert_alpha()
        self.weapon_display = pygame_gui.elements.UIImage(
            relative_rect = pygame.Rect(-128, -64, 128, 64),
            image_surface = weapon_display_image,
            anchors       = {"bottom": "bottom", "right": "right"},
            scale_func    = pygame.transform.scale
        )

    def update(self, dt, score, player_health, player_max_health,
               player_can_shoot, player_laser_shoot_time, player_cooldown_duration):
        """Update all UI elements with current game state."""
        # Validate input parameters
        if dt < 0:
            dt = 0
        if score < 0:
            score = 0
        if player_health < 0:
            player_health = 0
        if player_max_health <= 0:
            player_max_health = 1  # Prevent division by zero
        if player_health > player_max_health:
            player_health = player_max_health
        if player_cooldown_duration <= 0:
            player_cooldown_duration = 0.1  # Prevent division by zero

        self.ui_manager.update(dt)

        # Update score display
        self.score_label.set_text(f'Score: {score}')

        # Update health progress bar (value as percentage)
        health_percentage = (player_health / player_max_health) * 100
        self.health_bar.set_current_progress(health_percentage)

        # Update shooting cooldown progress bar
        if player_can_shoot:
            # Ready to shoot - show full bar
            self.cooldown_bar.set_current_progress(0)
        else:
            # Calculate remaining cooldown as percentage
            current_time = pygame.time.get_ticks()
            elapsed = (current_time - player_laser_shoot_time) / 1000
            remaining = max(0, player_cooldown_duration - elapsed)
            cooldown_percentage = (remaining / player_cooldown_duration) * 100
            # Show remaining cooldown directly (0% when ready, 100% when on cooldown)
            self.cooldown_bar.set_current_progress(cooldown_percentage)

    def draw(self, screen):
        """Draw all UI elements to the screen."""
        self.ui_manager.draw_ui(screen)

    def process_event(self, event):
        """Process pygame events for the UI manager."""
        self.ui_manager.process_events(event)