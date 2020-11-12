from ConfigLoader import ConfigLoader

class Region:
    def __init__(self, region_name):
        config_loader = ConfigLoader()
        regions_data = config_loader.load_config_file("regions")
        region_data = regions_data[region_name]

        self.x = region_data['start_x']
        self.padding = region_data['padding']
        self.width = region_data['width']

        self.mid_x = self.x + self.width / 2
        self.start_x_padded = self.x + self.padding
        self.width_padded = self.width - 2 * self.padding

    def process_y(self, y):
        self.y = y
        self.start_y_padded = self.y + self.padding

    def add_height(self, height):
        self.height = height
