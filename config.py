from configparser import ConfigParser


class ConfigReader (object):
    filename = "configuration.ini"

    def __init__(self, filename=None):
        if filename is not None:
            self.filename = filename

    def get_config(self, section):
        parser = ConfigParser()
        parser.read(self.filename)
        items = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                items[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, self.filename))
        return items