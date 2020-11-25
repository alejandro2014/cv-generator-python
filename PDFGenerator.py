import copy
import json

from fpdf import FPDF
from RegionManager import RegionManager
from Region import Region
from StringProcessor import StringProcessor
from ConfigLoader import ConfigLoader
from LineDrawer import LineDrawer

class PDFGenerator(FPDF):
    def __init__(self, company_name = '<UNKNOWN>'):
        super().__init__(unit = 'mm')
        self.__config_loader = ConfigLoader()
        self.pdf_fonts = self.__config_loader.fonts()
        self.font = None

        self.__region_manager = RegionManager()
        self.string_processor = StringProcessor()
        self.__line_drawer = LineDrawer(self)

        self.step_no = 1
        self.company_name = company_name

    def generate_cv(self, cv_data):
        self.add_page()

        self.draw_current_region()

        self.generate_header(cv_data['header'])
        self.generate_profile(cv_data['profile'])
        #self.generate_experiences(cv_data['experiences'])
        #self.generate_skills(cv_data['skills'])
        #self.generate_languages(cv_data['languages'])

        #self.company_mark()

    def generate_header(self, header):
        self.change_font('mainTitle')
        self.write_string_ln(header['name'], 'C')

        self.change_font('mainSubTitle')
        self.write_string_ln(header['position'], 'C')
        self.add_line()

        self.change_font('normalText')
        self.write_string_ln('Address: ' + header['address'], 'C')
        self.write_string_ln(header['mail'] + ', ' + header['phone'], 'C')
        self.write_string_ln('Place and date of birth: ' + header['birth']['date'] + ', ' + header['birth']['place'], 'C')

        self.add_line(2)

    def generate_profile(self, profile):
        self.change_font('sectionHeader')
        self.write_string_ln('Profile')

        self.change_font('normalText')
        self.write_paragraph(profile['introduction'])
        self.add_line()

    def write_paragraph(self, text):
        r = self.get_current_region()
        lines = self.get_paragraph_lines(text, r)

        for line in lines:
            self.write_string_ln(line)

    def write_string_ln(self, string, align = 'L'):
        self.write_string(string, align)
        self.add_line()

    def write_string(self, string, align = 'L'):
        r = self.__region_manager.region()

        if align == 'L':
            x = r.sxpad()
        elif align == 'C':
            string_width = self.get_string_width(string)
            x = r.mx() - (string_width / 2)

        self.text(x, r.cursor_y(), string)

    def add_line(self, lines_no = 1):
        r = self.__region_manager.region()

        for i in range(1, lines_no + 1):
            offset_y = self.font['size'] / 2.54
            r.inc_cursor_y(offset_y)

    def change_font(self, font_name):
        font = self.__config_loader.font(font_name)

        if font['style'] == 'bold':
            style = 'B'
        else:
            style = ''

        self.set_font(font['family'], style, font['size'])

        if self.font == None:
            r = self.get_current_region()
            r.inc_cursor_y(font['size'] / 2.54)

        self.font = font

    def draw_current_region(self):
        region = self.get_current_region()
        self.__line_drawer.draw_region(region)

    def get_current_region(self):
        return self.__region_manager.region()

    #---------------------------------------------------------------------

    def change_region(self, region_no):
        self.current_region = self.regions[region_no]

    def get_lowest_cursor(self):
        cy_left = self.regions[0].cursor_y()
        cy_right = self.regions[1].cursor_y()

        return cy_left if cy_left > cy_right else cy_right

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

        left_region.inc_cursor_y(self.font['size'] / 2.54)
        right_region.inc_cursor_y(self.font['size'] / 2.54)

        self.regions = [ left_region, right_region ]
        self.change_region(0)

    def generate_experiences(self, experiences):
        self.change_font('sectionHeader')
        self.write_string_ln('Work experiences')
        #self.__line_drawer.position_line()

        self.split_region('25%')
        #for experience in experiences:
        #    self.generate_experience(experience)
        self.generate_experience(experiences[0])
        #self.generate_experience(experiences[1])

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
        self.change_region(1)
        self.draw_right_cell(experience)

        self.change_region(0)
        self.draw_left_cell(experience)

    def draw_right_cell(self, experience):
        self.change_font('normalText')
        paragraphs = self.get_experience_paragraphs(experience)
        lines = self.get_paragraphs_lines(paragraphs)
        height = self.get_section_height(lines)

        self.current_region.set_height(height)
        #self.__line_drawer.position_line()
        #self.__line_drawer.draw_region(100.0)

        #if not self.is_experience_fitting(height):
        #    self.add_page()

        #self.current_region.add_height(height)
        #self.draw_region(self.current_region)

        self.write_lines(lines)
        self.__line_drawer.draw_region_border()

        #self.current_region.inc_cursor_y(height)
        #self.current_region.set_start_y(self.current_region.sy() + height)
        #print(height)
        self.__line_drawer.position_arrow()

    def draw_left_cell(self, experience):
        r = self.current_region
        #self.__line_drawer.draw_region(100.0)

        r.set_height(height)
        #self.__line_drawer.draw_region(100.0)

        logo_path = 'config/logos/' + experience['company']['id'] + '.png'
        self.image(logo_path, r.mx() - (42.0 - 5.0) / 2.54, r.cursor_y())

        self.add_line(3)
        experience_times = self.string_processor.get_experience_times(experience)
        self.write_string(experience_times, 'C')
        self.__line_drawer.draw_region_border()
        self.__line_drawer.position_arrow()

    def is_experience_fitting(self, height):
        return (self.current_y + height) <= 287.0

    def write_lines(self, lines):
        r = self.current_region

        for line in lines:
            self.write_string(line)
            r.inc_cursor_y(self.font['size'] / 2.54)

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

    def get_section_height(self, paragraph_lines):
        font = self.font
        height = (((len(paragraph_lines) + 1) * font['size']) / 2.54)

        return height

    def company_mark(self):
        self.change_font('smallText')
        company_mark = self.string_processor.get_company_mark(self.company_name)

        self.text(5.0, 293.0, company_mark)

        #self.change_font('normalText')
