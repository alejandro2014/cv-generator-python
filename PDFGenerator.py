import json

from fpdf import FPDF
from PIL import Image

from ConfigLoader import ConfigLoader
from LineDrawer import LineDrawer
from RegionManager import RegionManager
from Region import Region
from StringProcessor import StringProcessor

class Offset:
    def __init__(self):
        self.x = 0


class PDFGenerator(FPDF):
    def __init__(self, config_path, company_name=None, language='en'):
        super().__init__(unit = 'mm')
        self.__config_path = config_path
        self.__language = language
        self.__config_loader = ConfigLoader(config_path, language=self.__language)
        self.__cvdata = self.__config_loader.cvdata()
        self.font = None

        self.__region_manager = RegionManager()
        self.string_processor = StringProcessor()
        self.__line_drawer = LineDrawer(self)

        self.__exp_line_spacing = 4.0
        self.__line_spacing = 1.5
        self.step_no = 1
        self.company_name = company_name

    def render_document(self, document, document_data):
        self.__document = document
        self.__document_data = document_data
        self.add_page()

        #print(document)
        #print(document_data)

        x_min, y_min = coords_min = (0, 0)
        x_max, y_max = coords_max = (210, 297)
        x_mid, y_mid = coords_mid = ((x_max - x_min) / 2, (y_max - y_min) / 2)
        padding = 10

        coords_min_padded = (x_min + padding, y_min + padding)
        coords_max_padded = (x_max - padding, y_max - padding)

        self.draw_section_lines(coords_min, coords_max, coords_mid, coords_min_padded, coords_max_padded)

        lines = self.calculate_lines_size()

        self.draw_lines(lines, coords_min_padded[0], coords_max_padded[0], x_mid)

    def generate_cv(self):
        cv_data = self.__cvdata
        self.add_page()

        self.generate_header(cv_data['header'], cv_data)

        return
        self.generate_profile(cv_data['profile'])

        self.generate_skills(cv_data['skills'])
        self.generate_experiences(cv_data['experiences'])

        self.company_mark()

    def get_data_element(self, path):
        node = self.__cvdata

        path_elements = path.split('.')

        if path_elements[0] != '$':
            return ''

        for path_element in path_elements[1:]:
            node = node[path_element]

        return node

    def calculate_size(self, element):
        print(f'>>> {element}')
        return self.get_string_width(element['text'])
    
    def get_text_x(self, line, x_min, x_max, x_mid):
        align = line['align']

        if align == 'left':
            return x_min
        
        if align == 'center':
            return x_mid - line['total_length'] / 2
        
        if align == 'right':
            return x_max - line['total_length']
        
        return None
    
    def draw_section_border(self, coords_min, coords_max, coords_mid):
        x_min, y_min = coords_min
        x_max, y_max = coords_max
        x_mid, y_mid = coords_mid

        self.line(x_min, y_min, x_max, y_min)
        self.line(x_min, y_mid, x_max, y_mid)
        self.line(x_min, y_max, x_max, y_max)

        self.line(x_min, y_min, x_min, y_max)
        self.line(x_mid, y_min, x_mid, y_max)
        self.line(x_max, y_min, x_max, y_max)

    def draw_section_border_padding(self, coords_min_padded, coords_max_padded):
        x_min, y_min = coords_min_padded
        x_max, y_max = coords_max_padded

        self.line(x_min, y_min, x_max, y_min)
        self.line(x_min, y_max, x_max, y_max)

        self.line(x_min, y_min, x_min, y_max)
        self.line(x_max, y_min, x_max, y_max)

    def draw_section_lines(self, coords_min, coords_max, coords_mid, coords_min_padded, coords_max_padded):
        self.set_draw_color(0, 0, 0)
        self.draw_section_border(coords_min, coords_max, coords_mid)
        self.set_draw_color(150, 0, 0)
        self.draw_section_border_padding(coords_min_padded, coords_max_padded)
        self.set_draw_color(0, 0, 0)
    
    def calculate_lines_size(self):
        lines = self.__document['elements'][0]['lines']
        
        for line in lines:
            for element in line['elements']:
                font = self.get_element_font(element)

                self.set_font(font['family'], font['style'], font['size'])

                element['size'] = self.calculate_size(element)

            line['total_length'] = sum([ e['size'] for e in line['elements'] ])
            line['height'] = max([ self.get_element_font(e)['size'] for e in line['elements'] ])

        return lines
    
    def get_element_font(self, element):
        font_name = element['font']

        return self.__document['fonts'][font_name]
    
    def draw_text_element(self, element, x, y):
        font = self.get_element_font(element)
        
        self.set_font(font['family'], font['style'], font['size'])
        self.text(x, y, element['text'])

    def draw_text(self, line, x, y):
        for element in line['elements']:
            self.draw_text_element(element, x, y)
            
            x += element['size']

    def draw_lines(self, lines, x_min_padded, x_max_padded, x_mid):
        padding = 10

        for line in lines:
            x = self.get_text_x(line, x_min_padded, x_max_padded, x_mid)
            y = padding + line['height'] / 2.54

            self.draw_text(line, x, y)

        x_min, y_min = coords_min = (0, 0)
        x_max, y_max = coords_max = (210, 297)
        x_mid, y_mid = coords_mid = ((x_max - x_min) / 2, (y_max - y_min) / 2)
        padding = 10

        coords_min_padded = (x_min + padding, y_min + padding)
        coords_max_padded = (x_max - padding, y_max - padding)

        self.draw_section_lines(coords_min, coords_max, coords_mid, coords_min_padded, coords_max_padded)
        
        return
        self.change_font('mainTitle')
        string = self.get_data_element('$.header.name')
        self.write_string_ln(string, 'C')

        self.change_font('mainSubTitle')
        string = self.get_data_element('$.header.position')
        self.write_string_ln(string, 'C')

        string = self.get_data_element('$.header.repo')
        self.write_string_ln(string, 'C')

        self.add_line()

        self.change_font('normalText')
        self.write_string('Address: ', 'L')
        self.write_string_ln(header['address'], 'L')

        return
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

        logo_path = self.__config_path + '/logos/' + experience['company']['id'] + '.png'

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
            #self.__line_drawer.position_arrow()
            self.__line_drawer.draw_region(r)
            x = r.sxpad()
        elif align == 'C':
            string_width = self.get_string_width(string)
            x = r.mx() - (string_width / 2)

        self.text(x, r.cursor_y(), string)

    def add_line(self, lines_no = 1):
        r = self.get_current_region()

        for _ in range(1, lines_no + 1):
            offset_y = (self.font['size'] + self.__line_spacing) / 2.54
            r.inc_cursor_y(offset_y)

    def change_font(self, font_name):
        font = self.__config_loader.font(font_name)

        style = 'B' if font['style'] == 'bold' else ''

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
