from Region import Region

class Page:
    def __init__(self, pdf, region=Region()):
        self.pdf = pdf
        self.padding = padding

        self.region = Region()

    def draw_padding(self):
        pdf.rect(r.sx(), start_y, r.w(), r.h())
