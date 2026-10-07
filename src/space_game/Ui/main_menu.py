import pygame
import pygame_gui
from os.path import join
from space_game.ShipRepository import SHIP_REPOSITORY


class MainMenu:
    def __init__(self, screen):
        self.screen = screen

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.ships = list(SHIP_REPOSITORY.Ships.values())

        self.manager = pygame_gui.UIManager(
            (self.screen_width, self.screen_height)
        )

        self.state = "MAIN_MENU"
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

        self.select_ship_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                75, 350, 250, 60
            ),
            text="SELECT SHIP",
            manager=self.manager,
            container=self.ship_selection_panel
        )

    def handle_event(self, event):
        self.manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:

            if event.ui_element == self.previous_ship_button:
                print("PREVIOUS BUTTON PRESSED")
                self.selected_ship = (self.selected_ship - 1) % len(self.ships)
                self.update_ship_label()

            elif event.ui_element == self.next_ship_button:
                print("NEXT BUTTON PRESSED")
                self.selected_ship = (self.selected_ship + 1) % len(self.ships)
                self.update_ship_label()

            elif event.ui_element == self.select_ship_button:
                print("Selected ship:", self.ships[self.selected_ship].Name)

            elif event.ui_element == self.play_button:
                self.state = "GAME"

            elif event.ui_element == self.options_button:
                self.state = "OPTIONS"

            elif event.ui_element == self.quit_button:
                self.state = "QUIT"

    def update_ship_label(self):
            ship = self.ships[self.selected_ship]

            print("Ship index:", self.selected_ship)
            print("Ship name:", ship.Name)

            self.ship_label.set_text(ship.Name)
        
    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self):
        self.manager.draw_ui(self.screen)