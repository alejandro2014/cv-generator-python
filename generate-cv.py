import copy
import json
from fpdf import FPDF

#self.set_line_width(0.0)
#self.line(5.0, 10.0, 205.0, 10.0)
#self.line(5.0, 14.0, 205.0, 14.0)

def load_config_file(file_name):
    with open('config/' + file_name + '.json') as file:
        file_content = json.load(file)

    return file_content

class PDF(FPDF):
    def __init__(self):
        super().__init__(unit = 'mm')
        self.pdf_fonts = load_config_file('fonts')
        self.current_limits = { 'start_x': 10.0, 'end_x': 200.0 }
        self.current_x = self.current_limits['start_x']
        self.current_y = 30.0
        self.font = {}

    def generate_header(self, header):
        self.change_font('mainTitle')
        self.write_string(header['name'], 'C')
        self.new_line()

        self.change_font('mainSubTitle')
        self.write_string(header['position'], 'C')
        self.new_line()
        self.new_line()

        self.change_font('normalText')
        self.write_string('Address: ' + header['address'], 'C')
        self.new_line()

        self.write_string(header['mail'] + ', ' + header['phone'], 'C')
        self.new_line()

        self.write_string('Place and date of birth: ' + header['birth']['date'] + ', ' + header['birth']['place'], 'C')
        self.new_line()
        self.new_line()
        self.new_line()

    def generate_profile(self, profile):
        self.change_font('sectionHeader')
        self.write_string('Profile')
        self.new_line()

        self.change_font('normalText')
        self.write_paragraph(profile['introduction'])
        self.new_line()

    def generate_experiences(self, experiences):
        self.change_font('sectionHeader')
        self.write_string('Work experiences')
        self.new_line()

        width = 190.0

        self.set_line_width(0.0)
        self.rect(10.0, self.current_y, width * 0.3, 100.0)

        self.current_limits = { 'start_x': 10.0, 'end_x': width * 0.3 }
        self.current_x = self.current_limits['start_x']

        experience_times = self.generate_experience_times(experiences[0]['start'], experiences[0]['end'])
        #self.rect(10.0 + width * 0.3, self.current_y, width * 0.7, 100.0)

        self.change_font('normalText')
        self.new_line()

        self.write_string(experience_times, 'C')

    def generate_experience_times(self, start, end):
        return str(start) if start == end else str(start) + " - " + str(end)

    def write_paragraph(self, text):
        length = self.current_limits['end_x'] - self.current_limits['start_x']
        space_positions = [ pos for pos, char in enumerate(text) if char == ' ' ]
        lines = []
        start_space = 0

        for i in range(len(space_positions)):
            if self.get_string_width(text[start_space:space_positions[i]]) > length:
                lines.append(text[start_space:space_positions[i - 1]].strip())
                start_space = space_positions[i - 1]

        lines.append(text[start_space:len(text)].strip())

        for line in lines:
            self.write_string(line)
            self.new_line()

    def write_string(self, string, align = 'L'):
        if align == 'L':
            self.text(self.current_x, self.current_y, string)
        elif align == 'C':
            string_width = self.get_string_width(string)
            mid_x = (self.current_limits['end_x'] - self.current_limits['start_x']) + self.current_x
            current_x = self.current_x + ((mid_x - string_width) / 2)
            self.text(current_x, self.current_y, string)

    def change_font(self, font_name):
        current_font = copy.copy(self.pdf_fonts[font_name])

        if current_font['style'] == 'bold':
            current_font['style'] = 'B'
        else:
            current_font['style'] = ''

        self.set_font(current_font['family'], current_font['style'], current_font['size'])
        self.font = current_font

    def new_line(self):
        self.current_y += (self.font['size'] + 2.0) / 2.54
        self.current_x = self.current_limits['start_x']

cv_data = load_config_file('cv-data')

pdf = PDF()
pdf.add_page()

pdf.generate_header(cv_data['header'])
pdf.generate_profile(cv_data['profile'])
pdf.generate_experiences(cv_data['experiences'])
pdf.output('test.pdf','F')
