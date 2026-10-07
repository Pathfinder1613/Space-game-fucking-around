import pygame

from pygame.math import Vector2
from pygame.surface import Surface

from pathlib import Path

import json

class ShipData:
    def __init__(self: ShipData):
        self._set_defaults()

    def _set_defaults(self: ShipData):
        self.Name = str("Unnamed Ship")
        self.Visual: Surface = None

        self.Health   = int(100)
        self.Speed    = int(300)
        self.FireRate = float(0.5)

        self.FirePoints: dict[str, Vector2] = {}
        self.ThrustPoints: dict[str, Vector2] = {}

class ShipRepository:
    def __init__(self: ShipRepository):
        self.Ships: dict[str, ShipData] = {}
        self._load_all()

    def _load_all(self: ShipRepository):
        ship_path = Path("assets", "ships")

        data_folders = [f.name for f in ship_path.iterdir() if f.is_dir()]

        for ship_id in data_folders:
            ship_data = ShipData()
            ship_data.Visual = pygame.image.load(Path(ship_path, ship_id, "visual.png"))

            with open(Path(ship_path, ship_id, "data.json"), "r", encoding = "utf-8") as file:
                data = json.load(file)

                ship_data.Name = str(data["Name"])

                ship_data.Health   = int(data["Attributes"]["Health"])
                ship_data.Speed    = int(data["Attributes"]["Speed"])
                ship_data.FireRate = float(data["Attributes"]["FireRate"])

            self.Ships[ship_id] = ship_data

    def get_data(self: ShipRepository, id: str) -> ShipData | None:
        return self.Ships[id]