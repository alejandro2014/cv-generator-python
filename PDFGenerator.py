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
        #self.regions = [ Region.get_default_region() ]
        self.current_region = Region("main")

        self.configLoader = ConfigLoader()
        self.pdf_fonts = self.configLoader.load_config_file('fonts')

        self.string_processor = StringProcessor()

        self.cursor_y = 0.0
        self.current_y = 0.0
        self.step_no = 1
        self.company_name = company_name
        self.__line_drawer = LineDrawer(self)

    def generate_cv(self, cv_data):
        self.add_page()

        self.__line_drawer.draw_region(100.0)

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

    def generate_experiences(self, experiences):
        self.change_font('sectionHeader')
        self.write_string_ln('Work experiences')
        self.add_line()

        for experience in experiences:
            self.generate_experience(experience)

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
        current_y = self.current_y

        region_right = Region("rightColumn")
        region_left = Region("leftColumn")

        self.change_font('normalText')

        self.set_region(region_right)

        paragraphs = self.get_experience_paragraphs(experience)
        lines = self.get_paragraphs_lines(paragraphs, self.current_region)
        height = self.get_section_height(lines, self.font)

        if not self.is_experience_fitting(height):
            self.add_page()

            self.current_y = 10.0
            current_y = self.current_y

            self.set_region(region_right)

        self.current_region.add_height(height)
        self.draw_region(self.current_region)

        self.write_lines(lines)

        self.current_y = current_y

        self.set_region(region_left)

        self.current_region.add_height(height)
        self.draw_region(self.current_region)

        logo_path = 'config/logos/' + experience['company']['id'] + '.png'
        self.image(logo_path, self.current_region.mid_x - (42.0 - 5.0) / 2.54, self.current_y + 5.0)

        #self.add_line(4)
        experience_times = self.string_processor.get_experience_times(experience)
        self.write_string(experience_times, 'C')

        self.current_y += height
        self.cursor_y += height

    def is_experience_fitting(self, height):
        return (self.current_y + height) <= 287.0

    def write_lines(self, lines):
        for line in lines:
            self.write_string(line)
            self.cursor_y += (self.font['size'] / 2.54)

    def get_paragraphs_lines(self, paragraphs, region):
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
        height = self.get_section_height(lines, self.font)
        r.add_height(height)

        for line in lines:
            self.write_string_ln(line)

        self.add_line()

    def get_section_height(self, paragraph_lines, font):
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

        self.current_region.inc_y_cursor(font['size'] / 2.54)
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
