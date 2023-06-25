from src.infra.config_reader import ConfigReader
from dataclasses import dataclass
from definitions import ROOT_PATH
import os


@dataclass
class MyConfig:
    config_file = os.path.join(ROOT_PATH, 'config.ini')
    _reader = ConfigReader(config_file)

    # Yad 2 section
    yad2_url = _reader.get_value('yad2', 'url')
