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

    def write_paragraph(self, text, rect = { 'start_x': 10.0, 'end_x': 200.0 }):
        length = rect['end_x'] - rect['start_x']
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
            self.text(10.0, self.current_y, string)
        elif align == 'C':
            string_width = self.get_string_width(string)
            self.text((self.w - string_width) / 2, self.current_y, string)

    def change_font(self, font_name):
        self.font = self.pdf_fonts[font_name]

        if self.font['style'] == 'bold':
            self.font['style'] = 'B'
        else:
            self.font['style'] = ''

        self.set_font(self.font['family'], self.font['style'], self.font['size'])

    def new_line(self):
        self.current_y += (self.font['size'] + 2.0) / 2.54

cv_data = load_config_file('cv-data')

pdf = PDF()
pdf.add_page()

pdf.generate_header(cv_data['header'])
pdf.generate_profile(cv_data['profile'])
pdf.output('test.pdf','F')
