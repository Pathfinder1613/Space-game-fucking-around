import pygame
import pygame_gui
from os.path import join

class pause_meun():
    def __init__(self, screen_width, screen_height):
        """Initialize the pause menu UI elements."""
        self.ui_manager = pygame_gui.UIManager((screen_width, screen_height))
        # Load UI theme for better visuals
        try:
            self.ui_manager.get_theme().load_theme(join("assets", "ui_theme.json"))
        except FileNotFoundError:
            print("Warning: ui_theme.json not found, using default theme")
        except Exception as e:
            print(f"Error loading ui_theme.json: {e}")

        # Create pause label
        self.pause_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 100, screen_height // 2 - 50), (200, 50)),
            text='PAUSED',
            manager=self.ui_manager,
            object_id='#pause_label'
        )

        # Create instructions label
        self.instructions_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 150, screen_height // 2 + 20), (300, 30)),
            text='Press P to Resume',
            manager=self.ui_manager,
            object_id='#instructions_label'
        )

    def update(self, dt):
        """Update the UI elements."""
        self.ui_manager.update(dt)

    def draw(self, screen):
        """Draw the UI elements to the screen."""
        self.ui_manager.draw_ui(screen)