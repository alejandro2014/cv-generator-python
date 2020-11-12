import datetime

class StringProcessor:
    def __init__(self):
        self.repo = 'https://github.com/alejandro2014/cv-generator-python'

    def get_position_string(self, position):
        return "Position: " + position

    def get_company_string(self, company):
        return "Company: " + company['name'] + ", " + company['location'] + " - " + company['type'] + " - " + company['web']

    def get_technologies_string(self, technologies):
        return "Technologies: " +  ", ".join(technologies)

    def get_experience_times(self, experience):
        start = experience['start']
        end = experience['end']

        return str(start) if start == end else str(start) + " - " + str(end)

    def get_bullet_point_line(self, line):
        return "* " + line

    def get_company_mark(self, company):
        now = datetime.datetime.now()

        return now.strftime("%d/%m/%Y %H:%M:%S") + " - C.V. generado para " + company + " - " + self.repo
