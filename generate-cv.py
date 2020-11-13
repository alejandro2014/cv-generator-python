from ConfigLoader import ConfigLoader
from PDFGenerator import PDFGenerator

config_loader = ConfigLoader()
cv_data = config_loader.load_config_file('cv-data')

pdf = PDFGenerator()
pdf.generate_cv(cv_data)
pdf.output('test.pdf', 'F')
