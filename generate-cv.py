import datetime
import json
import os
import sys

from PDFGenerator import PDFGenerator

APP_CONFIG_PATH = f"{os.environ['PROGRAMS_CONFIG_PATH']}/cvs/config"

def read_config_variables(file):
    config_json_file = f"{APP_CONFIG_PATH}/{file}.json"

    with open(config_json_file, 'r') as config_file:
        config_vars = json.load(config_file)

    return config_vars

def generate_pdf_name(cv_data, company_name):
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")

    company = "" if company_name is None else f" - {company_name}"

    return f"CV {cv_data['header']['name']} - {date}{company}.pdf"

company_name = sys.argv[1] if len(sys.argv) > 1 else None

pdf = PDFGenerator(APP_CONFIG_PATH, company_name=company_name)
pdf.generate_cv()

cv_data = pdf.get_cv_data()
pdf_name = generate_pdf_name(cv_data, company_name)

config_vars = read_config_variables('cvs')
pdf_path = f"{config_vars['output_path']}/{pdf_name}"

pdf.output(pdf_path, 'F')
