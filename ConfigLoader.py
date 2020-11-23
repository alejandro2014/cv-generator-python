import json

class ConfigLoader:
    def __init__(self):
        self.__cvdata = self.load_config_file('cv-data')
        self.__fonts = self.load_config_file('fonts')

    def cvdata(self):
        return self.__cvdata

    def font(self, name):
        return self.__fonts[name]

    def load_config_file(self, file_name):
        with open('config/' + file_name + '.json') as file:
            file_content = json.load(file)

        return file_content
