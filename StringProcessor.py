class StringProcessor:
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

    def get_skill_line(self, skill):
        return "* " + skill
