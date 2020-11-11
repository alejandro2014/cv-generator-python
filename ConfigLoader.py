import json

class ConfigLoader:
    def load_config_file(self, file_name):
        with open('config/' + file_name + '.json') as file:
            file_content = json.load(file)

        return file_content
