import configparser


class ConfigReader:
    def __init__(self, file_path):
        self.config = configparser.ConfigParser()
        self.config.read(file_path)

    def get_value(self, section, key):
        try:
            value = self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = None
        return value
