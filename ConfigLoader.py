import json

class ConfigLoader:
    def __init__(self, config_path, language='en'):
        self.__config_path = config_path
        self.__cvdata = self.load_config_file(f'cv-data-{language}')
        self.__fonts = self.load_config_file('fonts')

    def cvdata(self):
        return self.__cvdata

    def fonts(self):
        return self.__fonts

    def font(self, name):
        return self.__fonts[name]

    def load_config_file(self, file_name):
        with open(f'{self.__config_path}/{file_name}.json') as file:
            file_content = json.load(file)

        return file_content
