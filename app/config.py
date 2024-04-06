import json
from dataclasses import dataclass


def read_config(filename):
    with open(filename, "r") as file:
        config = json.load(file)
    return config


@dataclass
class SettingFrame:
    def __init__(self, config_dict):
        self.width = config_dict["frame"]["width"]
        self.height = config_dict["frame"]["height"]
        self.geometry = f"{self.width}x{self.height}"
        self.button_size = config_dict["frame"]["button_size"]


@dataclass
class SettingVideo:
    def __init__(self, config_dict):
        self.max_width = config_dict["video"]["max_width"]
        self.max_height = config_dict["video"]["max_height"]


class Configuration:
    def __init__(
        self,
    ):
        config_dict = read_config("config.json")
        self.frame = SettingFrame(config_dict)
        self.video = SettingVideo(config_dict)
