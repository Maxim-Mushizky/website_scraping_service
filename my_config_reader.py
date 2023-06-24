from src.infra.config_reader import ConfigReader
from dataclasses import dataclass


@dataclass
class MyConfig:
    config_file = 'config.ini'
    _reader = ConfigReader(config_file)

    # Yad 2 section
    url = _reader.get_value('yad2', 'url')
