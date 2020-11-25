class LineDrawer:
    def __init__(self, pdf):
        self.__pdf = pdf

    def draw_region(self, r):
        pdf = self.__pdf

        height = 100.0
        end_y = r.sy() + height
        end_y_pad = r.sypad() + height

        # Outer edges
        pdf.line(r.sx(), r.sy(), r.ex(), r.sy())
        pdf.line(r.sx(), r.sy(), r.sx(), end_y)
        pdf.line(r.ex(), r.sy(), r.ex(), end_y)

        # Inner edges
        pdf.line(r.sxpad(), r.sypad(), r.expad(), r.sypad())
        pdf.line(r.sxpad(), r.sypad(), r.sxpad(), end_y_pad)
        pdf.line(r.expad(), r.sypad(), r.expad(), end_y_pad)

        # Mid point
        pdf.line(r.mx(), r.sy(), r.mx(), end_y)

    def draw_region_border(self):
        pdf = self.__pdf
        r = pdf.get_current_region()

        print("sx: " + str(r.sx()) + " sy: " + str(r.sy()) + " w: " + str(r.w()) + " h: " + str(r.h()))
        pdf.rect(r.sx(), r.sy(), r.w(), r.h())

    def position_line(self):
        pdf = self.__pdf
        r = pdf.get_current_region()

        pdf.line(10.0, r.cursor_y(), 189.0, r.cursor_y())

        #pdf.change_font('smallText')
        pdf.text(7.0, r.cursor_y() + 1, str(pdf.step_no))
        pdf.text(190.0, r.cursor_y() + 1, str(r.cursor_y()))

        pdf.step_no += 1

    def position_arrow(self):
        pdf = self.__pdf
        r = pdf.get_current_region()

        pdf.set_draw_color(150, 0, 0)
        pdf.line(3.0, r.cursor_y(), 18.0, r.cursor_y())
        pdf.line(18.0, r.cursor_y(), 18.0 - 4.0, r.cursor_y() - 2.0)
        pdf.line(18.0, r.cursor_y(), 18.0 - 4.0, r.cursor_y() + 2.0)
        pdf.set_draw_color(0, 0, 0)
