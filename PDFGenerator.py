import copy
import json
from fpdf import FPDF
from Region import Region
from StringProcessor import StringProcessor
from ConfigLoader import ConfigLoader
from LineDrawer import LineDrawer

class PDFGenerator(FPDF):
    def __init__(self, company_name = '<UNKNOWN>'):
        super().__init__(unit = 'mm')
        self.current_region = Region({
            "start_x": 0.0, "start_y": 0.0,
            "padding": 10.0, "width": 210.0
        })
        self.regions = [ self.current_region ]

        self.configLoader = ConfigLoader()
        self.pdf_fonts = self.configLoader.load_config_file('fonts')

        self.string_processor = StringProcessor()

        self.cursor_y = 0.0
        #self.current_y = 0.0
        self.step_no = 1
        self.company_name = company_name
        self.__line_drawer = LineDrawer(self)

    def change_region(self, region_no):
        self.current_region = self.regions[region_no]

    def region_data(self, sx, sy, pad, w):
        return {
            "start_x": sx,
            "start_y": sy,
            "padding": pad,
            "width": w
        }

    def split_region(self, percentage_string):
        percentage = float(percentage_string.replace('%', '')) / 100
        padding = 3.0

        r = self.current_region
        parent_width = r.wpad()
        parent_padding = r.padding()

        start_y = r.cursor_y()

        left_width = parent_width * percentage
        right_width = parent_width * (1 - percentage)
        left_x = parent_padding + r.sx()
        right_x = left_x + left_width

        left_data = self.region_data(left_x, start_y, padding, left_width)
        right_data = self.region_data(right_x, start_y, padding, right_width)

        left_region = Region(left_data)
        right_region = Region(right_data)

        left_region.inc_y_cursor(self.font['size'] / 2.54)
        right_region.inc_y_cursor(self.font['size'] / 2.54)

        self.regions = [ left_region, right_region ]
        self.change_region(0)

    def generate_cv(self, cv_data):
        self.add_page()

        self.__line_drawer.position_line()
        #self.__line_drawer.draw_region(100.0)

        self.generate_header(cv_data['header'])
        self.generate_profile(cv_data['profile'])
        self.generate_experiences(cv_data['experiences'])
        #self.generate_skills(cv_data['skills'])
        #self.generate_languages(cv_data['languages'])

        #self.company_mark()

    def generate_header(self, header):
        self.change_font('mainTitle')
        self.write_string_ln(header['name'], 'C')
        self.__line_drawer.position_line()

        self.change_font('mainSubTitle')
        self.write_string_ln(header['position'], 'C')
        self.__line_drawer.position_line()

        self.change_font('normalText')
        self.write_string_ln('Address: ' + header['address'], 'C')
        self.__line_drawer.position_line()

        self.write_string_ln(header['mail'] + ', ' + header['phone'], 'C')
        self.__line_drawer.position_line()

        self.write_string_ln('Place and date of birth: ' + header['birth']['date'] + ', ' + header['birth']['place'], 'C')
        self.__line_drawer.position_line()

        self.add_line(2)
        self.__line_drawer.position_line()

    def generate_profile(self, profile):
        self.change_font('sectionHeader')
        self.write_string_ln('Profile')
        self.__line_drawer.position_line()

        self.change_font('normalText')
        self.write_paragraph(profile['introduction'])
        self.__line_drawer.position_line()

    def generate_experiences(self, experiences):
        self.change_font('sectionHeader')
        self.write_string_ln('Work experiences')
        self.__line_drawer.position_line()

        #for experience in experiences:
        #    self.generate_experience(experience)
        self.generate_experience(experiences[0])

    def generate_skills(self, skills):
        self.generate_enumerated_section(skills, 'Skills')

    def generate_languages(self, languages):
        self.generate_enumerated_section(languages, 'Languages')

    def generate_enumerated_section(self, lines, title):
        self.change_font('sectionHeader')
        self.add_line()
        self.write_string_ln(title)
        self.add_line()

        self.change_font('normalText')

        for line in lines:
            current_line = self.string_processor.get_bullet_point_line(line)
            self.write_string_ln(current_line)

    def generate_experience(self, experience):
        self.split_region('25%')
        #self.__line_drawer.draw_region(100.0)

        self.change_font('normalText')
        self.change_region(1)

        paragraphs = self.get_experience_paragraphs(experience)
        lines = self.get_paragraphs_lines(paragraphs)
        height = self.get_section_height(lines)

        self.current_region.set_height(height)
        self.__line_drawer.draw_region_border()
        #self.__line_drawer.position_line()
        #self.__line_drawer.draw_region(100.0)

        #if not self.is_experience_fitting(height):
        #    self.add_page()

        #    self.current_y = 10.0
        #    current_y = self.current_y

        #    self.set_region(region_right)

        #self.current_region.add_height(height)
        #self.draw_region(self.current_region)

        self.write_lines(lines)

        #self.current_y = current_y
        return

        #self.set_region(region_left)

        #self.current_region.add_height(height)
        #self.draw_region(self.current_region)

        #logo_path = 'config/logos/' + experience['company']['id'] + '.png'
        #self.image(logo_path, self.current_region.mid_x - (42.0 - 5.0) / 2.54, self.current_y + 5.0)

        ##self.add_line(4)
        #experience_times = self.string_processor.get_experience_times(experience)
        #self.write_string(experience_times, 'C')

        #self.current_y += height
        #self.cursor_y += height

    def is_experience_fitting(self, height):
        return (self.current_y + height) <= 287.0

    def write_lines(self, lines):
        r = self.current_region

        for line in lines:
            self.write_string(line)
            r.inc_y_cursor(self.font['size'] / 2.54)

    def get_paragraphs_lines(self, paragraphs):
        region = self.current_region
        lines = []

        for paragraph in paragraphs:
            lines += (self.get_paragraph_lines(paragraph, region) + [ '' ])

        return lines

    def get_paragraph_lines(self, text, region):
        width = region.wpad()
        space_positions = [ pos for pos, char in enumerate(text) if char == ' ' ]
        lines = []
        start_space = 0

        for i in range(len(space_positions)):
            if self.get_string_width(text[start_space:space_positions[i]]) > width:
                lines.append(text[start_space:space_positions[i - 1]].strip())
                start_space = space_positions[i - 1]

        lines.append(text[start_space:len(text)].strip())

        return lines

    def get_experience_paragraphs(self, experience):
        paragraphs = []

        paragraphs.append(self.string_processor.get_company_string(experience['company']))
        paragraphs.append(self.string_processor.get_position_string(experience['position']))
        paragraphs.append(self.string_processor.get_technologies_string(experience['technologies']))

        return paragraphs

    def write_paragraph(self, text):
        r = self.current_region
        lines = self.get_paragraph_lines(text, r)
        height = self.get_section_height(lines)
        #r.add_height(height)

        for line in lines:
            self.write_string_ln(line)

        self.add_line()

    def get_section_height(self, paragraph_lines):
        font = self.font
        height = (((len(paragraph_lines) + 1) * font['size']) / 2.54)

        return height

    def write_string_ln(self, string, align = 'L'):
        self.write_string(string, align)
        self.add_line()

    def write_string(self, string, align = 'L'):
        r = self.current_region

        if align == 'L':
            x = r.sxpad()
        elif align == 'C':
            string_width = self.get_string_width(string)
            x = r.mx() - (string_width / 2)

        self.text(x, r.cursor_y(), string)

    def add_line(self, lines_no = 1):
        r = self.current_region

        for i in range(1, lines_no + 1):
            offset_y = self.font['size'] / 2.54
            r.inc_y_cursor(offset_y)
            #self.current_y += offset_y

    def change_font(self, font_name):
        font = copy.copy(self.pdf_fonts[font_name])

        if font['style'] == 'bold':
            font['style'] = 'B'
        else:
            font['style'] = ''

        self.set_font(font['family'], font['style'], font['size'])

        #self.current_region.inc_y_cursor(font['size'] / 2.54)
        self.font = font

    def set_region(self, region):
        region.process_y(self.current_y)
        self.current_region = region

        self.current_y = region.start_y_padded
        self.cursor_y = self.current_y + self.font['size'] / 2.54

    def company_mark(self):
        self.change_font('smallText')
        company_mark = self.string_processor.get_company_mark(self.company_name)

        self.text(5.0, 293.0, company_mark)
