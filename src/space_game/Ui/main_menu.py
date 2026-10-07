import pygame
import pygame_gui
from os.path import join

from pygame.surface import Surface 
from space_game.ship_repository import ShipRepository
from space_game.state import GameState

class MainMenu:
    def __init__(self: MainMenu, screen: Surface, ship_repository: ShipRepository):
        self.screen = screen

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.ships = list(ship_repository.Ships.values())

        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height))

        self.manager.add_font_paths(
            font_name = "oxanium",
            regular_path = "assets/fonts/Oxanium-Bold.ttf",
            bold_path = "assets/fonts/Oxanium-Bold.tff"
        )

        self.state = GameState.MAIN_MENU
        self.selected_ship = 0

        # MAIN MENU - LEFT SIDE
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                100, 250, 300, 60
            ),
            text="PLAY",
            manager=self.manager
        )

        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                100, 330, 300, 60
            ),
            text="OPTIONS",
            manager=self.manager
        )

        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                100, 410, 300, 60
            ),
            text="QUIT",
            manager=self.manager
        )

        # SHIP SELECTION - RIGHT SIDE
        self.ship_selection_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                750, 150, 400, 450
            ),
            manager=self.manager
        )

        self.ship_title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                50, 20, 300, 50
            ),
            text="SHIP SELECTION",
            manager=self.manager,
            container=self.ship_selection_panel
        )

        self.previous_ship_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(30, 100, 70, 60),
            text="<",
            manager=self.manager,
            container=self.ship_selection_panel
        )

        self.next_ship_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(300, 100, 70, 60),
            text=">",
            manager=self.manager,
            container=self.ship_selection_panel
        )
        self.ship_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                100, 100, 200, 60
            ),
            text=self.ships[self.selected_ship].Name,
            manager=self.manager,
            container=self.ship_selection_panel
        )

        self.ship_visual = pygame_gui.elements.UIImage(
            relative_rect = pygame.Rect(0, 80, 256, 256),
            manager = self.manager,
            parent_element = self.ship_selection_panel,
            container = self.ship_selection_panel,
            anchors = {"center": "center"},
            image_surface = pygame.surface.Surface((256, 256)).convert_alpha()
        )

        # self.select_ship_button = pygame_gui.elements.UIButton(
        #     relative_rect=pygame.Rect(
        #         75, 350, 250, 60
        #     ),
        #     text="SELECT SHIP",
        #     manager=self.manager,
        #     container=self.ship_selection_panel
        # )

        self.update_ship_label()

    def handle_event(self: MainMenu, event):

        self.manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                self.state = GameState.GAMEPLAY
            elif event.ui_element == self.options_button:
                self.state = GameState.SETTINGS
            elif event.ui_element == self.quit_button:
                self.state = GameState.EXITING
                pass
            elif event.ui_element == self.previous_ship_button:
                self.selected_ship -= 1

                if self.selected_ship < 0:
                    self.selected_ship = len(self.ships) - 1

                self.update_ship_label()

            elif event.ui_element == self.next_ship_button:
                self.selected_ship += 1

                if self.selected_ship > len(self.ships) - 1:
                    self.selected_ship = 0

                self.update_ship_label()


    def update_ship_label(self):
        ship_data = self.ships[self.selected_ship]
        self.ship_label.set_text(ship_data.Name)
        self.ship_visual.set_image(ship_data.Visual, scale_func = pygame.transform.scale)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self):
        self.manager.draw_ui(self.screen)
