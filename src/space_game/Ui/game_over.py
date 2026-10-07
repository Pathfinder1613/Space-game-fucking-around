import pygame
import pygame_gui
from os.path import join

class gameoverScreen:
    def __init__(self, screen_width, screen_height):
        """Initialize the game over screen UI elements."""
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

        # Load custom font for theme (verification)
        # self._load_custom_font_for_theme()

        self.game_over_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 100, screen_height // 2 - 50), (200, 50)),
            text='Game Over!',
            manager=self.ui_manager,
            object_id='#game_over_label'
        )
        self.score_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_width // 2 - 100, screen_height // 2), (200, 50)),
            text='Final Score: 0',
            manager=self.ui_manager,
            object_id='#final_score_label'
        )
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen_width // 2 - 75, screen_height // 2 + 60), (150, 50)),
            text='Restart',
            manager=self.ui_manager,
            object_id='#restart_button'
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen_width // 2 - 75, screen_height // 2 + 120), (150, 50)),
            text='Quit',        
            manager=self.ui_manager,
            object_id='#quit_button',
        )