class Region:
    def __init__(self, region_data):
        self.__start_x = region_data['start_x']
        self.__start_y = region_data['start_y']
        self.__width = region_data['width']
        self.__padding = region_data['padding']

        self.__end_x = self.__start_x + self.__width

        self.__start_x_padded = self.__start_x + self.__padding
        self.__start_y_padded = self.__start_y + self.__padding

        self.__end_x_padded = self.__end_x - self.__padding

        self.__mid_x = (self.__start_x + self.__end_x) / 2
        self.__width_padded = self.__width - 2 * self.__padding

        self.__cursor_y = self.__start_y + self.__padding

    def inc_y_cursor(self, offset):
        self.__cursor_y += offset

    def h(self):
        return self.__height

    def sx(self):
        return self.__start_x

    def sy(self):
        return self.__start_y

    def ex(self):
        return self.__end_x

    def sxpad(self):
        return self.__start_x_padded

    def sypad(self):
        return self.__start_y_padded

    def expad(self):
        return self.__end_x_padded

    def mx(self):
        return self.__mid_x

    def padding(self):
        return self.__padding

    def cursor_y(self):
        return self.__cursor_y

    def w(self):
        return self.__width

    def wpad(self):
        return self.__width_padded

    def set_height(self, h):
        self.__height = h
