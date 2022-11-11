from fpdf import FPDF
from PIL import Image

class RenderEngine(FPDF):
    def __init__(self):
        super().__init__(unit = 'mm')

    def draw_text(self, text, start, font=None):
        x, y = start

        font = {
            'name': 'times',
            'size': 12,
            'color': 'black',
            'style': 'regular'
        }

        style = 'B' if font['style'] == 'bold' else ''

        self.set_font(font['name'], style, font['size'])

        self.text(x, y, text)

    def draw_line(self, start, end, style=None):
        x1, y1 = start
        x2, y2 = end

        color = (150, 0, 0)
        r, g, b = color

        self.set_draw_color(r, g, b)

        self.line(x1, y1, x2, y2)

    def draw_image(self, path, start):
        x, y = start
        im = Image.open(path)
        width, height = im.size

        self.image(path, x, y)
