import copy
import json
from fpdf import FPDF
from Region import Region
from StringProcessor import StringProcessor
from ConfigLoader import ConfigLoader

class PDF(FPDF):
    def __init__(self):
        super().__init__(unit = 'mm')

        self.configLoader = ConfigLoader()
        self.pdf_fonts = self.configLoader.load_config_file('fonts')

        self.string_processor = StringProcessor()

        self.cursor_y = 0.0
        self.current_y = 0.0
        self.step_no = 1
        self.company_name = '<UNKNOWN>'

        self.change_font('normalText')

    def position_line(self):
        self.line(10.0, self.current_y, 189.0, self.current_y)

        self.change_font('smallText')
        self.text(7.0, self.current_y + 1, str(self.step_no))
        self.text(190.0, self.current_y + 1, str(self.current_y))
        self.step_no += 1

    def company_mark(self):
        self.change_font('smallText')
        company_mark = self.string_processor.get_company_mark(self.company_name)

        self.text(5.0, 293.0, company_mark)

    def generate_cv(self, cv_data):
        self.add_page()
        self.company_mark()

        region = Region("main")
        self.set_region(region)

        self.generate_header(cv_data['header'])
        self.generate_profile(cv_data['profile'])
        self.generate_experiences(cv_data['experiences'])
        self.generate_skills(cv_data['skills'])
        self.generate_languages(cv_data['languages'])

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
            self.company_mark()

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
        width = region.width_padded
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
        lines = self.get_paragraph_lines(text, self.current_region)
        height = self.get_section_height(lines, self.font)
        self.current_region.add_height(height)

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
        if align == 'L':
            x = self.current_region.start_x_padded
        elif align == 'C':
            string_width = self.get_string_width(string)
            x = self.current_region.mid_x - (string_width / 2)

        self.text(x, self.cursor_y, string)

    def change_font(self, font_name):
        current_font = copy.copy(self.pdf_fonts[font_name])

        if current_font['style'] == 'bold':
            current_font['style'] = 'B'
        else:
            current_font['style'] = ''

        self.set_font(current_font['family'], current_font['style'], current_font['size'])
        self.font = current_font

    def add_line(self, lines_no = 1):
        for i in range(1, lines_no + 1):
            offset_y = self.font['size'] / 2.54
            self.cursor_y += offset_y
            self.current_y += offset_y

    def set_region(self, region):
        region.process_y(self.current_y)
        self.current_region = region

        self.current_y = region.start_y_padded
        self.cursor_y = self.current_y + self.font['size'] / 2.54

    def draw_region(self, region):
        self.set_draw_color(0, 0, 0)
        self.rect(region.x, region.y, region.width, region.height)

config_loader = ConfigLoader()
cv_data = config_loader.load_config_file('cv-data')

pdf = PDF()
pdf.generate_cv(cv_data)
pdf.output('test.pdf', 'F')
