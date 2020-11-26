import datetime
import sys

from PDFGenerator import PDFGenerator

def generate_pdf_name(cv_data):
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")

    return "CV " + cv_data['header']['name'] + " - " + date + ".pdf"

company_name = sys.argv[1] if len(sys.argv) > 1 else None

pdf = PDFGenerator(company_name)
pdf.generate_cv()

cv_data = pdf.get_cv_data()
pdf_name = generate_pdf_name(cv_data)
pdf.output(pdf_name, 'F')
