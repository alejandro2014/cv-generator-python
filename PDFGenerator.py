import json

from fpdf import FPDF
from PIL import Image

from ConfigLoader import ConfigLoader
from LineDrawer import LineDrawer
from RegionManager import RegionManager
from Region import Region
from StringProcessor import StringProcessor

class PDFGenerator(FPDF):
    def __init__(self, company_name = None):
        super().__init__(unit = 'mm')
        self.__config_loader = ConfigLoader()
        self.__cvdata = self.__config_loader.cvdata()
        self.font = None

        self.__region_manager = RegionManager()
        self.string_processor = StringProcessor()
        self.__line_drawer = LineDrawer(self)

        self.__exp_line_spacing = 4.0
        self.__line_spacing = 1.5
        self.step_no = 1
        self.company_name = company_name

    def generate_cv(self):
        cv_data = self.__cvdata
        self.add_page()

        self.generate_header(cv_data['header'])
        self.generate_profile(cv_data['profile'])

        self.generate_skills(cv_data['skills'])
        self.generate_experiences(cv_data['experiences'])

        self.company_mark()

    def generate_header(self, header):
        self.change_font('mainTitle')
        self.write_string_ln(header['name'], 'C')

        self.change_font('mainSubTitle')
        self.write_string_ln(header['position'], 'C')
        self.write_string_ln(header['repo'], 'C')
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

        r = self.get_current_region()
        lines = self.get_paragraph_lines(profile['introduction'], r)
        self.write_paragraph(lines)
        self.add_line()

    def generate_experiences(self, experiences):
        self.change_font('sectionHeader')
        self.write_string_ln('Work experiences')

        self.__region_manager.split_region('25%')

        font_height = self.font['size'] / 2.54
        self.__region_manager.inc_region_cy(0, font_height)
        self.__region_manager.inc_region_cy(1, font_height)

        for experience in experiences:
            self.generate_experience(experience)

    def generate_experience(self, experience):
        self.__region_manager.change_region(1)

        self.change_font('normalText')
        lines = self.get_experience_lines(experience)
        height = self.get_section_height(lines)

        if not self.is_experience_fitting(height):
            self.add_page()
            start_y = 10.0
            self.__region_manager.set_sy(start_y)
            self.__region_manager.set_cy(start_y + self.font['size'] / 2.54)

        region = self.get_current_region()
        region.set_height(height)

        self.draw_right_cell(lines)

        self.__region_manager.change_region(0)
        region = self.get_current_region()
        region.set_height(height)

        self.draw_left_cell(experience)

        self.__region_manager.align_regions()
        self.__region_manager.inc_regions_cy(self.__exp_line_spacing)

    def get_experience_lines(self, experience):
        paragraphs = self.get_experience_paragraphs(experience)
        lines = self.get_paragraphs_lines(paragraphs)
        lines.append('')

        return lines

    def draw_right_cell(self, lines):
        region = self.get_current_region()
        start_y = region.cursor_y() - self.font['size'] / 1.28

        self.write_paragraph(lines)
        self.__line_drawer.draw_region_border(start_y)

    def draw_left_cell(self, experience):
        r = self.get_current_region()
        start_y = r.cursor_y() - self.font['size'] / 1.28

        logo_path = 'config/logos/' + experience['company']['id'] + '.png'

        im = Image.open(logo_path)
        width, height = im.size

        self.image(logo_path, r.mx() - ((width / 2.0) - 5.0) / 2.54, r.cursor_y())
        r.inc_cursor_y(height / 2.54 + 5.0)

        experience_times = self.string_processor.get_experience_times(experience)
        self.write_string(experience_times, 'C')
        self.__line_drawer.draw_region_border(start_y)

    def get_section_height(self, lines):
        lines_no = len(lines)
        spaces_no = lines_no - 1
        height = ((lines_no * self.font['size']) + (spaces_no * self.__line_spacing)) / 2.54

        return height

    def is_experience_fitting(self, height):
        r = self.__region_manager.current_region()

        return (r.cursor_y() + height) <= 287.0

    def get_experience_paragraphs(self, experience):
        paragraphs = []

        paragraphs.append(self.string_processor.get_company_string(experience['company']))
        paragraphs.append(self.string_processor.get_position_string(experience['position']))
        paragraphs.append(self.string_processor.get_technologies_string(experience['technologies']))

        return paragraphs

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

    def get_paragraphs_lines(self, paragraphs):
        region = self.get_current_region()
        lines = []

        for paragraph in paragraphs:
            lines += (self.get_paragraph_lines(paragraph, region) + [ '' ])

        return lines

    def write_paragraph(self, lines):
        for line in lines:
            self.write_string_ln(line)

    def write_string_ln(self, string, align = 'L'):
        self.write_string(string, align)
        self.add_line()

    def write_string(self, string, align = 'L'):
        r = self.get_current_region()

        if align == 'L':
            x = r.sxpad()
        elif align == 'C':
            string_width = self.get_string_width(string)
            x = r.mx() - (string_width / 2)

        self.text(x, r.cursor_y(), string)

    def add_line(self, lines_no = 1):
        r = self.get_current_region()

        for i in range(1, lines_no + 1):
            offset_y = (self.font['size'] + self.__line_spacing) / 2.54
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
        return self.__region_manager.current_region()

    def generate_skills(self, skills):
        self.generate_enumerated_section(skills, 'Skills')

    def generate_enumerated_section(self, lines, title):
        self.change_font('sectionHeader')
        self.write_string_ln(title)

        self.change_font('normalText')

        for line in lines:
            current_line = self.string_processor.get_bullet_point_line(line)
            self.write_string_ln(current_line)

        self.add_line()

    def company_mark(self):
        self.change_font('smallText')
        company_mark = self.string_processor.get_company_mark(self.company_name)

        self.text(5.0, 293.0, company_mark)

    def get_cv_data(self):
        return self.__cvdata
